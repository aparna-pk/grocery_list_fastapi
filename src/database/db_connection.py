from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker

from src.di.os_manager import USER_NAME, PASSWORD, DATABASE_NAME, HOST
from src.entity.grocery_list_entity import GroceryListEntity
from src.entity.grocery_list_user_entity import GroceryListUserEntity

connection_string = URL.create(
    'postgresql',
    username=USER_NAME,
    password=PASSWORD,
    host=HOST,
    database=DATABASE_NAME
)
engine = create_engine(connection_string)
Session = sessionmaker(bind=engine)
session = Session()

GroceryListEntity.metadata.create_all(engine)
GroceryListUserEntity.metadata.create_all(engine)
