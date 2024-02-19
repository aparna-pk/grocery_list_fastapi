from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm

from src.authentication.authentication import verify_password, create_access_token, create_refresh_token, \
    get_token_payload
from src.database.db_connection import session
from src.dto.grocery_list_user_dto import GroceryListUserDto
from src.dto.tokendto import Token
from src.entity.grocery_list_user_entity import GroceryListUserEntity

auth_router = APIRouter()


@auth_router.post("/token", tags=['authentication'])
def authenticate_user(data: OAuth2PasswordRequestForm = Depends()):
    user = session.query(GroceryListUserEntity).filter_by(user_name=data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")

    # Assuming verify_password takes username and password as arguments
    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Password incorrect")

    return get_user_token(user)


def get_user_token(user: GroceryListUserDto, refresh_token=None):
    if user.user_name is None:
        raise HTTPException(status_code=400, detail="invalid refresh token")
    payload = {
        "user_id": user.user_id,
        "username": user.user_name,
    }
    access_token_expiry = timedelta(minutes=30)
    access_token = create_access_token(payload, access_token_expiry)
    if not refresh_token:
        refresh_token = create_refresh_token(payload, access_token_expiry)
    return Token(access_token=access_token, refresh_token=refresh_token, expiry=access_token_expiry.seconds)


@auth_router.post('/refresh_token', tags=['authentication'])
def access_token_from_refresh_token(refresh_token: str = Header()):
    payload = get_token_payload(refresh_token)
    if not payload:
        raise HTTPException(status_code=400, detail="invalid refresh token")
    user_name = payload.get('username')
    user = session.query(GroceryListUserEntity).filter_by(user_name=user_name).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    return user

