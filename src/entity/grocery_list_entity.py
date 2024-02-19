from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from src.database.db_connection import Base
from src.entity.base_mixin import BaseMixin


class GroceryListEntity(Base, BaseMixin):
    __tablename__ = 'grocery_list'

    list_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String, nullable=True)
    list_name = Column(String, nullable=False)
    list_items = Column(JSONB, nullable=False)
    user_id = Column(Integer)
