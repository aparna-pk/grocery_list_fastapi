from typing import List, Optional

from fastapi import HTTPException, UploadFile

from src.authentication.authentication import get_password_hash
from src.database.db_connection import session, engine, Base
from src.di.os_manager import FILE_PATH, UPLOAD_PATH
from src.dto.grocery_list_dto import GroceryList
from src.dto.grocery_list_user_dto import GroceryListUserDto, ChangePassword
from src.entity.grocery_list_entity import GroceryListEntity
from src.entity.grocery_list_user_entity import GroceryListUserEntity
from src.entity.token_black_list import TokenBlacklist

Base.metadata.create_all(bind=engine)


class GroceryListRepository:
    @staticmethod
    def user_signup(user_details: GroceryListUserDto):
        user_details = GroceryListUserEntity(
            user_name=user_details.user_name,
            password=get_password_hash(user_details.password),
            email=user_details.email
        )
        try:
            session.add(user_details)
            session.commit()
            return {"message": "user successfully added"}
        except HTTPException:
            raise HTTPException(status_code=400, detail="something went wrong")

    @staticmethod
    def add_list_details(list_data: GroceryList, user_id: int):
        if list_data.list_name == "" or len(list_data.list_items) == 0 or any(i == "" for i in list_data.list_items):
            return {"message": "field can't be empty"}
        elif len(list_data.list_items) >= 15:
            return {"message": "limit of the list is 15 items"}
        existing_list = session.query(GroceryListEntity).filter_by(user_id=user_id,
                                                                   list_name=list_data.list_name,
                                                                   date=list_data.date).first()
        if existing_list:
            return {"message": "List with the same name and date already exists"}
        list_details = GroceryListEntity(
            date=list_data.date,
            list_name=list_data.list_name,
            list_items=list_data.list_items,
            user_id=user_id,
        )
        session.add(list_details)
        session.commit()
        return {"message": "list added successfully"}

    @staticmethod
    def list_details_by_name(list_name: str, user_id: int, date: Optional[str] = None):
        query = session.query(GroceryListEntity).filter_by(list_name=list_name, user_id=user_id)

        if date is not None:
            query = query.filter(GroceryListEntity.date == date)

        list_details = query.all()
        if not list_details:
            raise HTTPException(status_code=400, detail="list not exist")
        return list_details

    @staticmethod
    def change_password(data: ChangePassword):
        result = session.query(GroceryListUserEntity).filter_by(email=data.email).first()
        if result:
            result.password = get_password_hash(data.new_password)
            session.commit()
        if not result:
            raise HTTPException(status_code=400, detail="user not found")
        return {"message": "successfully updated"}

    @staticmethod
    def logout(token: str):
        # Add the token to the blacklist
        db_token = TokenBlacklist(token=token)
        # try:
        session.add(db_token)
        session.commit()
        return {"message": "successfully logout"}
        # except HTTPException:
        #     raise HTTPException(status_code=400, detail="something went wrong")

    async def upload_file(file: UploadFile):
        file_folder = FILE_PATH.join(UPLOAD_PATH, file.filename)
        with open(file_folder, "wb") as destination:
            destination.write(await file.read())
        return {"filename": file.filename}

    async def read_file(file_name: str):
        file_folder = FILE_PATH.join(UPLOAD_PATH, file_name)
        try:
            with open(file_folder, "r") as file:
                content = file.read()
            return {"file_content": content }
        except FileNotFoundError:
            return {"message": "File not found"}