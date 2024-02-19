from sqlalchemy import create_engine, URL
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from src.di.os_manager import USER_NAME, PASSWORD, DATABASE_NAME, HOST


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

Base = declarative_base()



