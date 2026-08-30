from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

from app import db
from app.models import Reservation, Resource


reservation_bp = Blueprint("reservation", __name__)


@reservation_bp.route("/reservations", methods=["POST"])
@jwt_required()
def create_reservation():
    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    resource_id = data.get("resource_id")
    reservation_date = data.get("reservation_date")
    start_time = data.get("start_time")
    end_time = data.get("end_time")
    purpose = data.get("purpose")

    if (
        resource_id is None
        or not reservation_date
        or not start_time
        or not end_time
    ):
        return jsonify({
            "success": False,
            "message": "Resource ID, reservation date, start time and end time are required"
        }), 400

    if not isinstance(resource_id, int):
        return jsonify({
            "success": False,
            "message": "Resource ID must be an integer"
        }), 400

    resource = db.session.get(Resource, resource_id)

    if not resource:
        return jsonify({
            "success": False,
            "message": "Resource not found"
        }), 404

    if resource.status != "AVAILABLE":
        return jsonify({
            "success": False,
            "message": "Resource is unavailable"
        }), 400

    try:
        reservation_date_value = datetime.strptime(
            reservation_date,
            "%Y-%m-%d"
        ).date()

        start_time_value = datetime.strptime(
            start_time,
            "%H:%M"
        ).time()

        end_time_value = datetime.strptime(
            end_time,
            "%H:%M"
        ).time()
    except ValueError:
        return jsonify({
            "success": False,
            "message": "Invalid date or time format. Use YYYY-MM-DD and HH:MM"
        }), 400

    if start_time_value >= end_time_value:
        return jsonify({
            "success": False,
            "message": "Start time must be before end time"
        }), 400

    user_id = int(get_jwt_identity())

    reservation = Reservation(
        user_id=user_id,
        resource_id=resource_id,
        reservation_date=reservation_date_value,
        start_time=start_time_value,
        end_time=end_time_value,
        purpose=purpose,
        status="CONFIRMED"
    )

    db.session.add(reservation)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Reservation created successfully",
        "reservation": {
            "id": reservation.id,
            "user_id": reservation.user_id,
            "resource_id": reservation.resource_id,
            "reservation_date": reservation.reservation_date.isoformat(),
            "start_time": reservation.start_time.strftime("%H:%M"),
            "end_time": reservation.end_time.strftime("%H:%M"),
            "purpose": reservation.purpose,
            "status": reservation.status,
            "created_at": reservation.created_at.isoformat()
            if reservation.created_at else None
        }
    }), 201


@reservation_bp.route("/reservations", methods=["GET"])
@jwt_required()
def get_reservations():
    user_id = int(get_jwt_identity())

    reservations = Reservation.query.filter_by(
        user_id=user_id
    ).order_by(
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
                "reservation_date": reservation.reservation_date.isoformat(),
                "start_time": reservation.start_time.strftime("%H:%M"),
                "end_time": reservation.end_time.strftime("%H:%M"),
                "purpose": reservation.purpose,
                "status": reservation.status,
                "created_at": reservation.created_at.isoformat()
                if reservation.created_at else None
            }
            for reservation in reservations
        ]
    }), 200


@reservation_bp.route("/reservations/<int:reservation_id>", methods=["GET"])
@jwt_required()
def get_reservation(reservation_id):
    user_id = int(get_jwt_identity())

    reservation = db.session.get(Reservation, reservation_id)

    if not reservation:
        return jsonify({
            "success": False,
            "message": "Reservation not found"
        }), 404

    if reservation.user_id != user_id:
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    return jsonify({
        "success": True,
        "reservation": {
            "id": reservation.id,
            "user_id": reservation.user_id,
            "resource_id": reservation.resource_id,
            "reservation_date": reservation.reservation_date.isoformat(),
            "start_time": reservation.start_time.strftime("%H:%M"),
            "end_time": reservation.end_time.strftime("%H:%M"),
            "purpose": reservation.purpose,
            "status": reservation.status,
            "created_at": reservation.created_at.isoformat()
            if reservation.created_at else None
        }
    }), 200


@reservation_bp.route("/reservations/<int:reservation_id>", methods=["DELETE"])
@jwt_required()
def cancel_reservation(reservation_id):
    user_id = int(get_jwt_identity())

    reservation = db.session.get(Reservation, reservation_id)

    if not reservation:
        return jsonify({
            "success": False,
            "message": "Reservation not found"
        }), 404

    if reservation.user_id != user_id:
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    if reservation.status == "CANCELLED":
        return jsonify({
            "success": False,
            "message": "Reservation is already cancelled"
        }), 400

    reservation.status = "CANCELLED"
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Reservation cancelled successfully",
        "reservation": {
            "id": reservation.id,
            "status": reservation.status
        }
    }), 200


@reservation_bp.route("/admin/reservations/<int:reservation_id>/status", methods=["PUT"])
@jwt_required()
def update_reservation_status(reservation_id):
    claims = get_jwt()

    if claims.get("role") != "ADMIN":
        return jsonify({
            "success": False,
            "message": "Admin access required"
        }), 403

    reservation = db.session.get(Reservation, reservation_id)

    if not reservation:
        return jsonify({
            "success": False,
            "message": "Reservation not found"
        }), 404

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "Request body is required"
        }), 400

    status = data.get("status")

    if status not in [
        "PENDING",
        "CONFIRMED",
        "CANCELLED",
        "COMPLETED"
    ]:
        return jsonify({
            "success": False,
            "message": "Invalid reservation status"
        }), 400

    reservation.status = status
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Reservation status updated successfully",
        "reservation": {
            "id": reservation.id,
            "user_id": reservation.user_id,
            "resource_id": reservation.resource_id,
            "reservation_date": reservation.reservation_date.isoformat(),
            "start_time": reservation.start_time.strftime("%H:%M"),
            "end_time": reservation.end_time.strftime("%H:%M"),
            "purpose": reservation.purpose,
            "status": reservation.status,
            "created_at": reservation.created_at.isoformat()
            if reservation.created_at else None
        }
    }), 200