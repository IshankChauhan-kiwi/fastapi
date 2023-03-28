from sqlalchemy import Column, Integer, String

from app.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, unique=True, primary_key=True, index=True)
    title = Column(String)
    body = Column(String)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, unique=True, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
