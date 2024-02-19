from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from src.authentication.authentication import oauth2_scheme, get_current_user
from src.dto.grocery_list_dto import GroceryList
from src.dto.grocery_list_user_dto import GroceryListUserDto, ChangePassword
from src.repository.grocery_list_repository import GroceryListRepository

router = APIRouter()
user_router = APIRouter(tags=['user'], dependencies=[Depends(oauth2_scheme)])


def get_user_id(user=Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=400, detail="USER NOT FOUNT")
    return user['data']['user_id']


class GroceryListUserController:
    @staticmethod
    @router.post("/sign_up/", tags=['signup'])
    def user_signup(user_details: GroceryListUserDto):
        return GroceryListRepository.user_signup(user_details)

    @staticmethod
    @user_router.post("/add_list_details/")
    def add_list_details(list_data: GroceryList, user_id=Depends(get_user_id)):
        return GroceryListRepository.add_list_details(list_data, user_id)

    @staticmethod
    @user_router.get("/user_list_by_name/{list_name}")
    def user_list_by_name(list_name: str, date: Optional[str] = None, user_id=Depends(get_user_id)):
        return GroceryListRepository.list_details_by_name(list_name, user_id, date)

    @staticmethod
    @router.post("/change_password")
    def change_password(data: ChangePassword):
        return GroceryListRepository.change_password(data)

    @staticmethod
    @user_router.post("/logout")
    def user_logout(token: str = Depends(oauth2_scheme)):
        return GroceryListRepository.logout(token)

    @router.post("/file_upload")
    async def upload_file(file: UploadFile = File(...)):
        return GroceryListRepository.upload_file(file)


    @router.get("/read_file")
    async def read_file(file_name: str):
        return GroceryListRepository.read_file(file_name)

