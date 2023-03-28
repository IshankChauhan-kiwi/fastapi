from datetime import datetime, timedelta

import jwt

ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24
ALGORITHM = "HS256"
JWT_SECRET_KEY = "ishank"
JWT_REFRESH_SECRET_KEY = "ishankchauhan"


def create_access_token(data: str):
    expiry = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    payload = {"exp": expiry, "user": str(data)}
    access_token = jwt.encode(payload, JWT_SECRET_KEY, ALGORITHM)
    return access_token


def create_refresh_token(data: str):
    expiry = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    payload = {"exp": expiry, "user": str(data)}
    refresh_token = jwt.encode(payload, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return refresh_token
