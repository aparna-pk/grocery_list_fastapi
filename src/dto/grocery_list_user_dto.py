from pydantic import BaseModel


class GroceryListUserDto(BaseModel):
    user_name: str
    password: str
    email: str


class ChangePassword(BaseModel):
    email: str
    new_password: str
