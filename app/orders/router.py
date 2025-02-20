from fastapi import APIRouter, Depends, HTTPException

from app.orders.dao import OrdersDAO
from app.orders.schemas import SOrderResponse
from app.tasks.tasks import send_order_confirmation_email
from app.users.dependencies import get_current_user
from app.users.models import Users
from app.exceptions import CannotMakeOrderWithoutAddress, CannotMakeOrderWithoutItems, NotEnoughProductsInStock

router = APIRouter(
    prefix="/orders",
    tags=["Заказы"]
)


@router.get("")
async def get_orders(user: Users = Depends(get_current_user)):
    return await OrdersDAO.find_all(user_id=user.id)


@router.post("/checkout")
async def make_order(user: Users = Depends(get_current_user)) -> SOrderResponse:
    if user.delivery_address is None:
        raise CannotMakeOrderWithoutAddress

    try:
        order = await OrdersDAO.make_order(user_id=user.id)
    except NotEnoughProductsInStock:
        raise HTTPException(status_code=400, detail="Недостаточно товара на складе")

    if not order:
        raise CannotMakeOrderWithoutItems

    order_response = SOrderResponse.model_validate(order)

    # Отправка письма с подтверждением
    send_order_confirmation_email.delay(order_response.model_dump(), user.email)
    return order_response
