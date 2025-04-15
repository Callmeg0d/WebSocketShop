from sqlalchemy import update

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.users.models import Users


class UsersDAO(BaseDAO):
    model = Users

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            new_user = cls.model(**data)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

    @classmethod
    async def change_address(cls, new_address: str, user_id: int):
        async with async_session_maker() as session:
            await session.execute(
                update(Users).
                where(Users.id == user_id).
                values(delivery_address=new_address)
            )
            await session.commit()
            return new_address

    @classmethod
    async def change_name(cls, new_name: str, user_id: int):
        async with async_session_maker() as session:
            await session.execute(
                update(Users).where(Users.id == user_id).values(name=new_name)
            )
            await session.commit()
            return new_name
