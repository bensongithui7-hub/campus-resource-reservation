import os
from datetime import timedelta
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

    DATABASE_URL = os.getenv("DATABASE_URL")

    if DATABASE_URL:
        if DATABASE_URL.startswith("mysql://"):
            DATABASE_URL = DATABASE_URL.replace(
                "mysql://", "mysql+pymysql://", 1
            )

        parsed = urlparse(DATABASE_URL)
        query = dict(parse_qsl(parsed.query))

        query.pop("ssl-mode", None)

        DATABASE_URL = urlunparse(
            parsed._replace(query=urlencode(query))
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
