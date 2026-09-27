from pygments.token import Number
from sqlalchemy import Column, Integer, String
from src.config.db import Base

class Item(Base):
    __tablename__ = "customers"
    # name = Column(Integer, primary_key=True, index=True)
    name=Column(String, primary_key=True, index=True)
    category = Column(String, index=True)
    address = Column(String, index=True)
    opening_balance = Column(Number, index=True)

    __tablename__ = "item"
    name=Column(String, primary_key=True, index=True)
    tax = Column(Number, index=True)
