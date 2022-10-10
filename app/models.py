import enum
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class ItType(enum.Enum):
    SMARTPHONE = "SMARTPHONE"
    TV = "TV"
    LAPTOP = "LAPTOP"


class Item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    it_type = Column(Enum(ItType), nullable=False)
    price = Column(Integer, nullable=False)
    photo_url = Column(String(255), nullable=False)
