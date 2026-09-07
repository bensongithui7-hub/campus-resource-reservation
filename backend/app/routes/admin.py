from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt

from app import db
from app.models import CheckIn, Notification, Reservation, Resource, User


admin_bp = Blueprint("admin", __name__)


def admin_required():
    claims = get_jwt()

    if claims.get("role") != "ADMIN":
        return jsonify({
            "success": False,
            "message": "Admin access required"
        }), 403

    return None

@admin_bp.route("/admin/reservations", methods=["GET"])
@jwt_required()
def get_all_reservations():
    access_error = admin_required()

    if access_error:
        return access_error

    reservations = Reservation.query.order_by(
        Reservation.reservation_date,
        Reservation.start_time
    ).all()

    return jsonify({
        "success": True,
        "reservations": [
            {
                "id": reservation.id,
                "user_id": reservation.user_id,
                "resource_id": reservation.resource_id,
                "resource_name": (
                    db.session.get(Resource, reservation.resource_id).name
                    if db.session.get(Resource, reservation.resource_id)
                    else None
                ),
                "reservation_date": reservation.reservation_date.isoformat(),
                "start_time": reservation.start_time.strftime("%H:%M"),
                "end_time": reservation.end_time.strftime("%H:%M"),
                "purpose": reservation.purpose,
                "status": reservation.status,
                "created_at": (
                    reservation.created_at.isoformat()
                    if reservation.created_at else None
                )
            }
            for reservation in reservations
        ]
    }), 200

@admin_bp.route("/admin/check-ins", methods=["GET"])
@jwt_required()
def get_all_check_ins():
    access_error = admin_required()

    if access_error:
        return access_error

    check_ins = CheckIn.query.order_by(
        CheckIn.id
    ).all()

    return jsonify({
        "success": True,
        "check_ins": [
            {
                "id": check_in.id,
                "reservation_id": check_in.reservation_id,
                "qr_token": check_in.qr_token,
                "status": check_in.status,
                "checked_in_at": (
                    check_in.checked_in_at.isoformat()
                    if check_in.checked_in_at else None
                )
            }
            for check_in in check_ins
        ]
    }), 200


@admin_bp.route("/admin/users", methods=["GET"])
@jwt_required()
def get_all_users():
    access_error = admin_required()

    if access_error:
        return access_error

    users = User.query.order_by(User.id).all()

    return jsonify({
        "success": True,
        "users": [
            {
                "id": user.id,
                "name": user.name,
                "student_id": user.student_id,
                "email": user.email,
                "role": user.role,
                "created_at": (
                    user.created_at.isoformat()
                    if user.created_at else None
                )
            }
            for user in users
        ]
    }), 200


@admin_bp.route(
    "/admin/resources/<int:resource_id>/status",
    methods=["PUT"]
)
@jwt_required()
def update_resource_status(resource_id):
    access_error = admin_required()

    if access_error:
        return access_error

    resource = db.session.get(Resource, resource_id)

    if not resource:
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404

    data = request.get_json()

    if not data or "status" not in data:
        return jsonify({
            "success": False,
            "message": "Status is required"
        }), 400

    status = data.get("status")

    if status not in ["AVAILABLE", "UNAVAILABLE"]:
        return jsonify({
            "success": False,
            "message": "Invalid resource status"
        }), 400

    resource.status = status
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Resource status updated successfully",
        "resource": {
            "id": resource.id,
            "name": resource.name,
            "status": resource.status
        }
    }), 200

@admin_bp.route(
    "/admin/reservations/<int:reservation_id>/status",
    methods=["PUT"]
)
@jwt_required()
def update_reservation_status(reservation_id):
    access_error = admin_required()

    if access_error:
        return access_error

    reservation = db.session.get(Reservation, reservation_id)

    if not reservation:
        return jsonify({
            "success": False,
            "message": "Reservation not found"
        }), 404

    data = request.get_json()

    if not data or "status" not in data:
        return jsonify({
            "success": False,
            "message": "Status is required"
        }), 400

    status = data.get("status")
    current_status = reservation.status

    allowed_transitions = {
        "PENDING": ["CONFIRMED", "CANCELLED"],
        "CONFIRMED": ["COMPLETED", "CANCELLED"],
        "CANCELLED": [],
        "COMPLETED": []
    }

    if status not in allowed_transitions:
        return jsonify({
            "success": False,
            "message": "Invalid reservation status"
        }), 400

    if status not in allowed_transitions[current_status]:
        return jsonify({
            "success": False,
            "message": (
                f"Cannot change reservation status from "
                f"{current_status} to {status}"
            )
        }), 400

    reservation.status = status

    print("NOTIFICATION DEBUG:", reservation.id, reservation.user_id, status)

    resource = db.session.get(Resource, reservation.resource_id)

    if status == "CONFIRMED":
        message = (
            f"Your reservation for "
            f"{resource.name if resource else 'the requested resource'} "
            f"has been confirmed."
        )

        notification = Notification(
            user_id=reservation.user_id,
            reservation_id=reservation.id,
            message=message,
            type="RESERVATION_CONFIRMED"
        )

        db.session.add(notification)
        print("NOTIFICATION CREATED:", notification.id, notification.user_id, notification.type)

    elif status == "CANCELLED":
        message = (
            f"Your reservation for "
            f"{resource.name if resource else 'the requested resource'} "
            f"has been cancelled."
        )

        notification = Notification(
            user_id=reservation.user_id,
            reservation_id=reservation.id,
            message=message,
            type="RESERVATION_CANCELLED"
        )

        db.session.add(notification)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Reservation status updated successfully",
        "reservation": {
            "id": reservation.id,
            "status": reservation.status
        }
    }), 200