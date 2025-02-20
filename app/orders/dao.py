from sqlalchemy import select, func, delete, literal_column, update, case

from app.dao.base import BaseDAO
from app.exceptions import NotEnoughProductsInStock
from app.orders.models import Orders
from app.database import async_session_maker
from app.products.models import Products
from app.shopping_carts.models import ShoppingCarts
from app.users.models import Users


class OrdersDAO(BaseDAO):
    model = Orders

    @classmethod
    async def make_order(cls, user_id):
        async with async_session_maker() as session:
            # Получаем товары в корзине пользователя
            cart_query = (
                select(ShoppingCarts.product_id, ShoppingCarts.quantity)
                .where(ShoppingCarts.user_id == user_id)
            )
            cart_result = await session.execute(cart_query)
            cart_items = cart_result.mappings().all()

            # Получаем текущее количество товаров на складе
            product_ids = [item["product_id"] for item in cart_items]
            stock_query = (
                select(Products.product_id, Products.product_quantity)
                .where(Products.product_id.in_(product_ids))
            )

            stock_result = await session.execute(stock_query)
            stock_items = {item["product_id"]: item["product_quantity"] for item in stock_result.mappings().all()}

            for item in cart_items:
                product_id = item["product_id"]
                requested_quantity = item["quantity"]
                available_quantity = stock_items.get(product_id, 0)

                if requested_quantity > available_quantity:
                    raise NotEnoughProductsInStock

            query = (
                select(
                    Users.id.label('user_id'),
                    func.now().label("order_date"),
                    literal_column("'Arriving'").label('status'),
                    Users.delivery_address.label("delivery_address"),
                    func.jsonb_agg(
                        func.jsonb_build_object('product_id', ShoppingCarts.product_id,
                                                'quantity', ShoppingCarts.quantity)
                    ).label("order_items"),
                    func.sum(ShoppingCarts.total_cost).label("total_cost")
                )
                .join(ShoppingCarts, Users.id == ShoppingCarts.user_id)
                .where(Users.id == user_id)
                .group_by(Users.id, Users.delivery_address)
            )

            result = await session.execute(query)
            order = result.first()

            orders_item = Orders(
                user_id=user_id,
                created_at=order.order_date.replace(microsecond=0),
                status=order.status,
                delivery_address=order.delivery_address,
                order_items=order.order_items,
                total_cost=order.total_cost
            )
            session.add(orders_item)

            # Уменьшаем количество товара после заказа
            update_query = (
                update(Products)
                .where(Products.product_id.in_(product_ids))
                .values(
                    product_quantity=case(
                        *[(Products.product_id == item["product_id"], Products.product_quantity - item["quantity"])
                          for item in cart_items]
                    )
                )
            )
            await session.execute(update_query)

            # Очищаем корзину пользователя
            delete_query_cart = delete(ShoppingCarts).where(ShoppingCarts.user_id == user_id)
            await session.execute(delete_query_cart)

            await session.commit()
            await session.refresh(orders_item)
            return orders_item
