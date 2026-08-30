from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), unique=True, nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(
        db.Enum("STUDENT", "ADMIN"),
        nullable=False,
        default="STUDENT"
    )
    created_at = db.Column(
        db.DateTime,
        server_default=db.func.current_timestamp()
    )