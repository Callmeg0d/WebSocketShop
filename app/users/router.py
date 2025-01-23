from fastapi import APIRouter
from fastapi import Response
from app.users.auth import get_password_hash, create_access_token
from app.users.schemas import SUserAuth
from app.users.dao import UsersDAO
from app.users.auth import authenticate_user
from app.exceptions import UserAlreadyExistsException, IncorrectEmailOrPasswordException


router = APIRouter(
    prefix="/auth",
    tags=["Auth & Пользователи"]
)


@router.post("/register")
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    if existing_user:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, name=user_data.name, hashed_password=hashed_password)


@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({"sub": str(user.id)})
    #Помещаем созданный токен в куки
    response.set_cookie("access_token", access_token, max_age=1800, httponly=True) #max_age для удаления куков, при истичении действия expire(в сек.)
    return {"access_token": access_token}
