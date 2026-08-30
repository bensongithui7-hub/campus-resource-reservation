from app import db


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    resource_id = db.Column(
        db.Integer,
        db.ForeignKey("resources.id"),
        nullable=False
    )

    reservation_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)

    purpose = db.Column(db.String(255), nullable=True)

    status = db.Column(
        db.Enum(
            "PENDING",
            "CONFIRMED",
            "CANCELLED",
            "COMPLETED"
        ),
        nullable=False,
        default="CONFIRMED"
    )

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )