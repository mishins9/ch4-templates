from typing import Optional

from sqlalchemy import func
from sqlalchemy.future import select

from data.user import User

from passlib.handlers.sha2_crypt import sha512_crypt as crypto

from data import db_session


# def user_count() -> int:
#     return 73_874
#
#
# def create_account(name: str, email: str, password: str) -> User:
#     return User(name, email, 'abc')
#
#
# def login_user(email: str, password: str) -> Optional[User]:
#     if password == 'abc':
#         return User("test user", email, 'abc')
#
#     return None

# def user_count() -> int:
#     session = db_session.create_session()
#
#     try:
#         return session.query(User).count()
#     finally:
#         session.close()

async def user_count() -> int:
    async with db_session.create_async_session() as session:
        query = select(func.count(User.id))
        result = await session.execute(query)
        return result.scalar()


# def create_account(name: str, email: str, password: str) -> User:
#     session = db_session.create_session()
#
#     try:
#         user = User()
#         user.email = email
#         user.name = name
#         user.hash_password = crypto.hash(password, rounds=172_434)
#
#         session.add(user)
#         session.commit()
#
#         return user
#     finally:
#         session.close()
async def create_account(name: str, email: str, password: str) -> User:
    user = User()
    user.email = email
    user.name = name
    user.hash_password = crypto.hash(password, rounds=172_434)

    async with db_session.create_async_session() as session:
        session.add(user)
        await session.commit()

    return user


# def login_user(email: str, password: str) -> Optional[User]:
#     session = db_session.create_session()
#
#     try:
#         user = session.query(User).filter(User.email == email).first()
#         if not user:
#             return user
#
#         if not crypto.verify(password, user.hash_password):
#             return None
#
#         return user
#     finally:
#         session.close()
async def login_user(email: str, password: str) -> Optional[User]:
    async with db_session.create_async_session() as session:
        query = select(User).filter(User.email == email)
        results = await session.execute(query)

        user = results.scalar_one_or_none()
        if not user:
            return user

        try:
            if not crypto.verify(password, user.hash_password):
                return None
        except ValueError:
            return None

        return user


# def get_user_by_id(user_id: int) -> Optional[User]:
#     session = db_session.create_session()
#
#     try:
#         return session.query(User).filter(User.id == user_id).first()
#     finally:
#         session.close()
async def get_user_by_id(user_id: int) -> Optional[User]:
    async with db_session.create_async_session() as session:
        query = select(User).filter(User.id == user_id)
        result = await session.execute(query)

        return result.scalar_one_or_none()


# def get_user_by_email(email: str) -> Optional[User]:
#     session = db_session.create_session()
#
#     try:
#         return session.query(User).filter(User.email == email).first()
#     finally:
#         session.close()
async def get_user_by_email(email: str) -> Optional[User]:
    async with db_session.create_async_session() as session:
        query = select(User).filter(User.email == email)
        result = await session.execute(query)

        return result.scalar_one_or_none()
