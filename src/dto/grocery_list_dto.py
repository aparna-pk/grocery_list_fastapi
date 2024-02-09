from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ValidationError, field_validator


class GroceryList(BaseModel):

    list_name: str
    date: Optional[str]
    list_items: List[str]

    @field_validator('date')
    def validate_date_format(cls, value):
        if value == "":
            return value
        date_format = '%d-%m-%Y'
        try:
            datetime.strptime(value, date_format)
        except ValueError:
            raise ValueError("Incorrect data format, should be DD-MM-YYYY")
        return value
