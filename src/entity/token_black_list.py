from sqlalchemy import Integer, Column, String

from src.database.db_connection import Base
from src.entity.base_mixin import BaseMixin


class TokenBlacklist(Base, BaseMixin):
    __tablename__ = 'token_blacklist'

    token_id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String, nullable=False)
