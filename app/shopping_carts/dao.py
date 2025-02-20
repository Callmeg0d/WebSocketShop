from sqlalchemy import update, select, delete
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

    @classmethod
    async def get_cart_items(cls, user_id: int):
        async with async_session_maker() as session:
            query = (
                select(
                    ShoppingCarts.product_id,
                    Products.name,
                    Products.description,
                    Products.price,
                    ShoppingCarts.quantity,
                    (Products.price * ShoppingCarts.quantity).label("total_cost"),
                    Products.product_quantity
                )
                .join(Products, ShoppingCarts.product_id == Products.product_id)
                .where(ShoppingCarts.user_id == user_id)
            )
            result = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def remove_from_cart(cls, user_id: int, product_id: int):
        async with async_session_maker() as session:
            query = delete(ShoppingCarts).where(
                ShoppingCarts.user_id == user_id,
                ShoppingCarts.product_id == product_id
            )
            result = await session.execute(query)
            await session.commit()
            return result.rowcount > 0

    @classmethod
    async def update_quantity(cls, user_id, product_id, quantity):
        async with async_session_maker() as session:
            query = (
                update(ShoppingCarts)
                .where(ShoppingCarts.user_id == user_id, ShoppingCarts.product_id == product_id)
                .values(quantity=quantity, total_cost=Products.price * quantity)
                .returning(ShoppingCarts.total_cost)
            )
            result = await session.execute(query)
            await session.commit()
            return result.fetchone()