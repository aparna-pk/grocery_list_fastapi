from typing import Optional

from fastapi import APIRouter, Depends

from src.authentication.authentication import oauth2_scheme, get_current_user
from src.dto.grocery_list_dto import GroceryList
from src.repository.grocery_list_repository import GroceryListRepository

router = APIRouter()
user_router = APIRouter(tags=['user'], dependencies=[Depends(oauth2_scheme)])


def get_user_id(user=Depends(get_current_user)):
    return user['data']['user_id']


class GroceryListUserController:
    @staticmethod
    @router.post("/sign_up/{user_name}/{password}", tags=['signup'])
    def user_signup(user_name: str, password: str, email: str):
        return GroceryListRepository.user_signup(user_name, password, email)

    @staticmethod
    @user_router.post("/add_list_details/")
    def add_list_details(list_data: GroceryList, user_id=Depends(get_user_id)):
        return GroceryListRepository.add_list_details(list_data, user_id)

    @staticmethod
    @user_router.get("/user_list_by_name/{list_name}")
    def user_list_by_name(list_name: str, date: Optional[str] = None, user_id=Depends(get_user_id)):
        return GroceryListRepository.list_details_by_name(list_name, user_id, date)

    @staticmethod
    @router.post("/login/{user}")
    def login(username: str, password: str):
        return GroceryListRepository.login(username, password)

