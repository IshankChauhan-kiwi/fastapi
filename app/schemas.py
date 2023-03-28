from pydantic import BaseModel


class Value(BaseModel):
    title: str
    body: str


class Data(BaseModel):
    name: str
    email: str
    password: str
