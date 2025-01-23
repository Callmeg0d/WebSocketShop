from fastapi import APIRouter, Depends

from app.orders.dao import OrdersDAO
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/orders",
    tags=["Заказы"]
)


@router.get("")
async def get_orders(user: Users = Depends(get_current_user)):
    return await OrdersDAO.find_all(user_id=user.id)


@router.post("")
async def make_order(user: Users = Depends(get_current_user)):
    if user.delivery_address is None:
        raise "Укажите адрес доставки"
    return await OrdersDAO.make_order(user_id=user.id)
