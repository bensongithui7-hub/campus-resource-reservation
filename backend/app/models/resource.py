from app import db


class Resource(db.Model):
    __tablename__ = "resources"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(
        db.Enum("LABORATORY", "STUDY_ROOM", "EQUIPMENT"),
        nullable=False
    )
    description = db.Column(db.Text, nullable=True)
    location = db.Column(db.String(150), nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=1)
    status = db.Column(
        db.Enum("AVAILABLE", "UNAVAILABLE"),
        nullable=False,
        default="AVAILABLE"
    )
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )