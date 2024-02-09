from pydantic import BaseModel


class GroceryListUserDto(BaseModel):

    user_name: str
    password: str
