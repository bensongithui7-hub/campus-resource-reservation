from app import db


class CheckIn(db.Model):
    __tablename__ = "check_ins"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    reservation_id = db.Column(
        db.Integer,
        db.ForeignKey("reservations.id"),
        nullable=False,
        unique=True
    )

    qr_token = db.Column(
        db.String(255),
        nullable=False,
        unique=True
    )

    checked_in_at = db.Column(
        db.DateTime,
        nullable=True
    )

    status = db.Column(
        db.Enum("NOT_CHECKED_IN", "CHECKED_IN"),
        nullable=False,
        default="NOT_CHECKED_IN"
    )