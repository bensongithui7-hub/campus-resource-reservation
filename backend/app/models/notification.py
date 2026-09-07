from datetime import datetime

from app import db


class Notification(db.Model):
    __tablename__ = "notifications"

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    reservation_id = db.Column(
        db.Integer,
        db.ForeignKey("reservations.id"),
        nullable=True
    )

    message = db.Column(
        db.String(255),
        nullable=False
    )

    type = db.Column(
        db.String(50),
        nullable=False
    )

    is_read = db.Column(
        db.Boolean,
        default=False,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = db.relationship(
        "User",
        backref="notifications"
    )

    reservation = db.relationship(
        "Reservation",
        backref="notifications"
    )