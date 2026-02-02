from http import HTTPStatus

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from src.database import get_session
from src.models import User
from src.schemas import UserList, UserPublic, UserSchema

app = FastAPI(title='Aplicacao Boa')


@app.post('/users/', status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        if db_user.username == user.username:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Username ja cadastrado',
            )
        if db_user.email == user.email:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='Email ja cadastrado',
            )

    new_user = User(
        username=user.username,
        email=user.email,
        password=user.password,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def read_users(session=Depends(get_session), limit: int = 10, offset: int = 0):
    users = session.scalars(select(User).limit(limit).offset(offset))
    return {'users': users}


@app.put(
    '/users/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
)
def update_user(user_id: int, user: UserSchema, session=Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='ID nao encontrado na base de dados',
        )
    try:
        user_db.username = user.username
        user_db.email = user.email
        user_db.password = user.password

        session.add(user_db)
        session.commit()
        session.refresh(user_db)

        return user_db
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='Username ou email ja cadastrado',
        )


@app.delete('/users/{user_id}', status_code=HTTPStatus.OK)
def delete_user(user_id: int, session=Depends(get_session)):

    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='ID nao encontrado na base de dados',
        )

    session.delete(user_db)
    session.commit()
    return {'message': 'User deleted successfully'}


# @app.get(
#     '/user/{user_id}', status_code=HTTPStatus.OK, response_model=UserPublic
# )
# def get_user(user_id: int):
#     if user_id > len(database) or user_id < 1:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail='ID nao encontrado na base de dados',
#         )
#     return database[user_id - 1]
