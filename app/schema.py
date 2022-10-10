from enum import Enum
from pydantic import BaseModel


class ItemType(str, Enum):
    SMARTPHONE = "SMARTPHONE"
    TV = "TV"
    LAPTOP = "LAPTOP"


class Item(BaseModel):
    name: str
    it_type: ItemType
    price: int
    photo_url: str

    class Config:
        orm_mode = True
