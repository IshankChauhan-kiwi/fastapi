from fastapi import FastAPI, Depends, HTTPException
from starlette import status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Item, User
from app.schemas import Value, Data
from . import models
from .database import engine
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm
from .token import create_access_token, create_refresh_token
from sqladmin import Admin, ModelView


models.Base.metadata.create_all(engine)
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


app = FastAPI()
admin = Admin(app, engine)


class ItemAdmin(ModelView, model=Item):
    column_list = [Item.id, Item.title]


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.name]


admin.add_view(ItemAdmin)
admin.add_view(UserAdmin)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post('/item', status_code=status.HTTP_201_CREATED, tags=['item'])
def create(request: Value, db: Session = Depends(get_db)):
    item = Item(title=request.title, body=request.body)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {'success': item}


@app.get("/items", status_code=status.HTTP_200_OK, tags=['item'])
def get_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return {'items': items}


@app.get("/items/{item_id}", status_code=status.HTTP_200_OK, tags=['item'])
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    return {'item': item}


@app.put("/items/{item_id}", status_code=status.HTTP_200_OK, tags=['item'])
def update_items(item_id: int, request: Value,  db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id)
    print(item)
    item.update({Item.title: request.title, Item.body: request.body})
    db.commit()
    return {'success': "item updated successfully"}


@app.post('/signup', status_code=status.HTTP_201_CREATED, tags=['user'])
def create(request: Data, db: Session = Depends(get_db)):
    hash_pass = password_context.hash(request.password)
    user = User(name=request.name, email=request.email, password=hash_pass)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {'success': user}


@app.post('/login', status_code=status.HTTP_200_OK, tags=['user'])
def user_login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.username).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Email not found')

    if not password_context.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Incorrect password')

    return {'access_token': create_access_token(user.id), 'refresh_token': create_refresh_token(user.id),
            'token_type': 'bearer'}


@app.get("/users", status_code=status.HTTP_200_OK, tags=['user'])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return {'users': users}


@app.get("/user/{user_id}", status_code=status.HTTP_200_OK, tags=['user'])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return {'user': user}


@app.put("/user/{user_id}", status_code=status.HTTP_200_OK, tags=['user'])
def update_user(user_id: int, request: Data,  db: Session = Depends(get_db)):
    hash_pass = password_context.hash(request.password)
    user = db.query(models.User).filter(models.User.id == user_id)
    user.update({User.name: request.name, User.email: request.email, User.password: hash_pass})
    db.commit()
    return {'success': "user updated successfully"}
