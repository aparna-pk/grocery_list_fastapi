from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class GroceryListEntity(Base):
    __tablename__ = 'grocery_list'

    list_id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String, nullable=True)
    list_name = Column(String, nullable=False)
    list_items = Column(JSONB, nullable=False)
    user_id = Column(Integer)



