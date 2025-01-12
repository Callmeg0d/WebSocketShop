from fastapi import APIRouter, Depends

from app.shopping_carts.dao import CartsDAO

from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/cart",
    tags=["Корзина"]
)


@router.get("")
async def get_cart(user: Users = Depends(get_current_user)):
    return await CartsDAO.find_all(user_id=user.id)