from fastapi.responses import JSONResponse
from fastapi import APIRouter, Response, Depends
from jose import jwt, JWTError
import jwt
from app.config import settings
from app.users.auth import get_password_hash, create_access_token, create_refresh_token
from app.users.dependencies import get_refresh_token
from app.users.schemas import SUserAuth
from app.users.dao import UsersDAO
from app.users.auth import authenticate_user
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException
from fastapi import Request
from app.exceptions import TokenExpiredException
from jwt.exceptions import  InvalidTokenError
from datetime import datetime, timedelta
from app.tasks.tasks import send_registration_confirmation_email

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

router_users = APIRouter(
    prefix="/users",
    tags=["Пользователи"],
)


@router_auth.post('/register')
async def register_user(user_data: SUserAuth):
    # Проверяем существование юзера
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)

    # Отправка письма с подтверждением
    send_registration_confirmation_email.delay(user_data.email)

    return JSONResponse(content={"message": "User created successfully"}, status_code=201)


@router_auth.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException

    access_token = create_access_token({"sub": str(user.id)})
    refresh_token = create_refresh_token({"sub": str(user.id)})

    response.set_cookie("access_token", access_token, max_age=1800, httponly=True, samesite="lax")
    response.set_cookie("refresh_token", refresh_token, max_age=604800, httponly=True, samesite="lax")

    return {"access_token": access_token, "refresh_token": refresh_token}


@router_auth.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("access_token")


@router_auth.post("/refresh")
async def refresh_token(response: Response, token: str = Depends(get_refresh_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
    except JWTError:
        raise InvalidTokenError

    # Проверяем, не истёк ли refresh токен
    expire = payload.get("exp")
    if not expire or int(expire) < datetime.utcnow().timestamp():
        raise TokenExpiredException

    user_id = payload.get("sub")
    if not user_id:
        raise InvalidTokenError

    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user or user_id == "None":
        raise InvalidTokenError

    # Создаём новый access token
    new_access_token = jwt.encode(
        {"sub": str(user.id), "exp": datetime.utcnow() + timedelta(minutes=30)},
        settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )

    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")

    response.set_cookie("access_token", new_access_token, max_age=1800, httponly=True, samesite="lax")
    response.set_cookie("refresh_token", token, max_age=604800, httponly=True, samesite="lax")

    return {"access_token": new_access_token}
