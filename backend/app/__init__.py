from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS

from app.config import Config

db = SQLAlchemy()
jwt = JWTManager()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)

    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    jwt.init_app(app)
    CORS(
        app,
        origins=[
            "http://localhost:5173",
            "http://localhost:5174",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:5174",
            "https://campus-resource-reservation.vercel.app",
            "https://campus-resource-reservation-2vz5.vercel.app",
    ],
)

    from app.routes.health import health_bp
    app.register_blueprint(health_bp, url_prefix="/api")

    from app.routes.auth import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/api")

    from app.routes.protected import protected_bp
    app.register_blueprint(protected_bp, url_prefix="/api")

    from app.routes.resource import resource_bp
    app.register_blueprint(resource_bp, url_prefix="/api")

    from app.routes.reservation import reservation_bp
    app.register_blueprint(reservation_bp, url_prefix="/api")

    from app.routes.check_in import check_in_bp
    app.register_blueprint(check_in_bp, url_prefix="/api")

    from app.routes.notification import notification_bp
    app.register_blueprint(notification_bp, url_prefix="/api")

    from app.routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix="/api")

    return app