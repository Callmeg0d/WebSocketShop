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
