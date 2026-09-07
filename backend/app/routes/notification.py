from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app import db
from app.models import User, Notification


notification_bp = Blueprint("notification", __name__)


@notification_bp.route("/notifications", methods=["GET"])
@jwt_required()
def get_notifications():
    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    notifications = (
        Notification.query
        .filter_by(user_id=user.id)
        .order_by(Notification.created_at.desc())
        .all()
    )

    return jsonify({
        "success": True,
        "notifications": [
            {
                "id": notification.id,
                "reservation_id": notification.reservation_id,
                "message": notification.message,
                "type": notification.type,
                "is_read": notification.is_read,
                "created_at": notification.created_at.isoformat()
            }
            for notification in notifications
        ]
    }), 200


@notification_bp.route(
    "/notifications/<int:notification_id>/read",
    methods=["PUT"]
)
@jwt_required()
def mark_notification_read(notification_id):
    user_id = get_jwt_identity()

    user = db.session.get(User, int(user_id))

    if not user:
        return jsonify({
            "success": False,
            "message": "User not found"
        }), 404

    notification = Notification.query.filter_by(
        id=notification_id,
        user_id=user.id
    ).first()

    if not notification:
        return jsonify({
            "success": False,
            "message": "Notification not found"
        }), 404

    notification.is_read = True
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Notification marked as read"
    }), 200