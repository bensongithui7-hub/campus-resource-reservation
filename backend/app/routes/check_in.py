import secrets
from datetime import datetime, timezone

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import CheckIn, Reservation


check_in_bp = Blueprint("check_in", __name__)


@check_in_bp.route("/reservations/<int:reservation_id>/check-in", methods=["POST"])
@jwt_required()
def generate_check_in(reservation_id):
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

    if reservation.status != "CONFIRMED":
        return jsonify({
            "success": False,
            "message": "Only confirmed reservations can be checked in"
        }), 400

    existing_check_in = CheckIn.query.filter_by(
        reservation_id=reservation.id
    ).first()

    if existing_check_in:
        return jsonify({
            "success": True,
            "message": "Check-in token already exists",
            "check_in": {
                "id": existing_check_in.id,
                "reservation_id": existing_check_in.reservation_id,
                "qr_token": existing_check_in.qr_token,
                "status": existing_check_in.status,
                "checked_in_at": (
                    existing_check_in.checked_in_at.isoformat()
                    if existing_check_in.checked_in_at else None
                )
            }
        }), 200

    qr_token = secrets.token_urlsafe(32)

    check_in = CheckIn(
        reservation_id=reservation.id,
        qr_token=qr_token,
        status="NOT_CHECKED_IN"
    )

    db.session.add(check_in)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Check-in token generated successfully",
        "check_in": {
            "id": check_in.id,
            "reservation_id": check_in.reservation_id,
            "qr_token": check_in.qr_token,
            "status": check_in.status,
            "checked_in_at": None
        }
    }), 201


@check_in_bp.route("/check-in/<string:qr_token>", methods=["POST"])
@jwt_required()
def perform_check_in(qr_token):
    check_in = CheckIn.query.filter_by(
        qr_token=qr_token
    ).first()

    if not check_in:
        return jsonify({
            "success": False,
            "message": "Invalid check-in token"
        }), 404

    if check_in.status == "CHECKED_IN":
        return jsonify({
            "success": False,
            "message": "Already checked in"
        }), 400

    reservation = db.session.get(
        Reservation,
        check_in.reservation_id
    )

    if not reservation:
        return jsonify({
            "success": False,
            "message": "Reservation not found"
        }), 404

    user_id = int(get_jwt_identity())

    if reservation.user_id != user_id:
        return jsonify({
            "success": False,
            "message": "Access denied"
        }), 403

    if reservation.status != "CONFIRMED":
        return jsonify({
            "success": False,
            "message": "Only confirmed reservations can be checked in"
        }), 400

    check_in.status = "CHECKED_IN"
    check_in.checked_in_at = datetime.now(timezone.utc).replace(tzinfo=None)

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Check-in successful",
        "check_in": {
            "id": check_in.id,
            "reservation_id": check_in.reservation_id,
            "qr_token": check_in.qr_token,
            "status": check_in.status,
            "checked_in_at": check_in.checked_in_at.isoformat()
        }
    }), 200


@check_in_bp.route("/reservations/<int:reservation_id>/check-in", methods=["GET"])
@jwt_required()
def get_check_in(reservation_id):
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

    check_in = CheckIn.query.filter_by(
        reservation_id=reservation_id
    ).first()

    if not check_in:
        return jsonify({
            "success": False,
            "message": "Check-in record not found"
        }), 404

    return jsonify({
        "success": True,
        "check_in": {
            "id": check_in.id,
            "reservation_id": check_in.reservation_id,
            "qr_token": check_in.qr_token,
            "status": check_in.status,
            "checked_in_at": (
                check_in.checked_in_at.isoformat()
                if check_in.checked_in_at else None
            )
        }
    }), 200
