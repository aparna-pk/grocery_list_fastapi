import os

from dotenv import load_dotenv

load_dotenv()

# database details
USER_NAME = os.getenv("USER_NAME")
PASSWORD = os.getenv("PASSWORD")
DATABASE_NAME = os.getenv("DB_NAME")
HOST = os.getenv("HOST")

# authentication details
JWT_SECRET = os.getenv("SECRET")
JWT_ALGORITHM = os.getenv("ALGORITHM")

