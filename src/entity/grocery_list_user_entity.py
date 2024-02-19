from sqlalchemy import Column, Integer, String

from src.database.db_connection import Base
from src.entity.base_mixin import BaseMixin


class GroceryListUserEntity(Base, BaseMixin):
    __tablename__ = 'grocery_list_user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String, nullable=False)
