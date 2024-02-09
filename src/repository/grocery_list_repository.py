from typing import List, Optional

from fastapi import HTTPException

from src.authentication.authentication import get_password_hash, get_current_user
from src.database.db_connection import session
from src.dto.grocery_list_dto import GroceryList
from src.entity.grocery_list_entity import GroceryListEntity
from src.entity.grocery_list_user_entity import GroceryListUserEntity


class GroceryListRepository:
    @staticmethod
    def user_signup(username: str, password: str):
        user_details = GroceryListUserEntity(
            user_name=username,
            password=get_password_hash(password)
        )
        session.add(user_details)
        session.commit()
        return {"message": "user successfully added"}

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
