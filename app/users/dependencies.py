from fastapi import Request, HTTPException, status, Depends
from jose import jwt, JWTError
from datetime import datetime
from app.config import settings


from app.users.dao import UsersDAO


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try: #декодим токен и достаём данные из payload
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    expire: str = payload.get("exp")  #достали время истечения токена
    if (not expire) or int(expire) < datetime.utcnow().timestamp():
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user_id: str = payload.get("sub")  #достали id
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
