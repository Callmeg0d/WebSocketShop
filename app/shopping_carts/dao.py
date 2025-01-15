from sqlalchemy import update, select
from app.products.models import Products
from app.database import async_session_maker

from app.shopping_carts.models import ShoppingCarts
from app.dao.base import BaseDAO


class CartsDAO(BaseDAO):
    model = ShoppingCarts

    @classmethod
    async def add_to_cart(cls, product_id: int, user_id: int, quantity: int):
        async with async_session_maker() as session:
            result = await session.execute(
                select(Products.price, Products.product_quantity).where(Products.product_id == product_id)
            )
            product = result.first()
            if not product or product.product_quantity < quantity:
                raise ValueError("Недостаточно товара на складе")

            price = product.price
            total_cost = price * quantity

            # Проверка наличия товара в корзине
            existing_cart_item = await session.execute(
                select(ShoppingCarts).where(ShoppingCarts.user_id == user_id,
                                            ShoppingCarts.product_id == product_id)
            )
            cart_item = existing_cart_item.scalar_one_or_none()

            if cart_item:
                await session.execute(
                    update(ShoppingCarts)
                    .where(ShoppingCarts.user_id == user_id, ShoppingCarts.product_id == product_id)
                    .values(
                        quantity=ShoppingCarts.quantity + quantity,
                        total_cost=ShoppingCarts.total_cost + total_cost
                    )
                )
            else:
                new_cart_item = ShoppingCarts(
                    user_id=user_id,
                    product_id=product_id,
                    quantity=quantity,
                    total_cost=total_cost
                )
                session.add(new_cart_item)
            await session.commit()
