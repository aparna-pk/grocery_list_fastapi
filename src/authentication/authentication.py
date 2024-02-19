from datetime import timedelta, datetime, timezone
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from starlette.authentication import AuthCredentials, UnauthenticatedUser

from src.database.db_connection import session
from src.di.os_manager import JWT_SECRET, JWT_ALGORITHM
from src.dto.grocery_list_user_dto import GroceryListUserDto
from src.entity.grocery_list_user_entity import GroceryListUserEntity
from src.entity.token_black_list import TokenBlacklist

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def get_token_payload(token):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGORITHM)
    except JWTError:
        return None
    return payload


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    if is_token_blacklisted(token):
        return {"message": "USER NOT LOGIN"}
    payload = get_token_payload(token)
    if not payload or type(payload) is not dict:
        return {"message": "Could not validate credentials"}

    user_id = payload.get('user_id', None)
    if user_id is None:
        return {"message": "Could not validate credentials"}

    user_details = session.query(GroceryListUserEntity).filter_by(user_id=user_id).first()
    if user_details:
        user_info = {
            "user_id": user_details.user_id,
            "username": user_details.user_name,
            "password": user_details.password
        }
        return {"data": user_info}
    else:
        return {"message": "User not found"}

def is_token_blacklisted(token: str):
    # Check if the token is blacklisted
    return session.query(TokenBlacklist).filter(TokenBlacklist.token == token).first() is not None

# class JWTAuth:
#     async def authenticate(self, conn):
#         guest = AuthCredentials(['unauthenticated']), UnauthenticatedUser()
#         if 'authorization' not in conn.headers:
#             return guest
#         token = conn.headers.get('authorization').split(' ')[1]  # Bearer token hash
#         if not token:
#             return guest
#
#         user = get_current_user(token)
#         if user is None:
#             return guest
#         return AuthCredentials(['authenticated']), user
