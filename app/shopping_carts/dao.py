from app.shopping_carts.models import ShoppingCarts
from app.dao.base import BaseDAO


class CartsDAO(BaseDAO):
    model = ShoppingCarts
