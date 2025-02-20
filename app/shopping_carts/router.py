from fastapi import APIRouter, Depends, Body

from app.exceptions import CannotHaveLessThan1Product, NeedToHaveAProductToIncreaseItsQuantity
from app.shopping_carts.dao import CartsDAO

from app.users.dependencies import get_current_user
from app.users.models import Users
from app.shopping_carts.schemas import SShoppingCart, UpdateQuantityRequest

router = APIRouter(
    prefix="/cart",
    tags=["Корзина"]
)


@router.get("")
async def get_cart(user: Users = Depends(get_current_user)):
    return await CartsDAO.find_all(user_id=user.id)


@router.post("")
async def add_to_cart(user: Users = Depends(get_current_user),
                      cart: SShoppingCart = Body(...)):
    result = await CartsDAO.add_to_cart(product_id=cart.product_id, user_id=user.id, quantity=cart.quantity)
    return result


@router.delete("/remove/{product_id}")
async def remove_from_cart(product_id: int, user: Users = Depends(get_current_user)):
    await CartsDAO.remove_from_cart(user_id=user.id, product_id=product_id)
    return {"message": "Товар удален"}


@router.put("/update/{product_id}")
async def update_cart_item(
    product_id: int,
    request: UpdateQuantityRequest,
    user: Users = Depends(get_current_user)
):
    if request.quantity < 1:
        raise CannotHaveLessThan1Product

    updated_item = await CartsDAO.update_quantity(user.id, product_id, request.quantity)
    if not updated_item:
        raise NeedToHaveAProductToIncreaseItsQuantity

    return {"total_cost": updated_item.total_cost}