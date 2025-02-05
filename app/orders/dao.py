from sqlalchemy import select, func, delete, literal_column

from app.dao.base import BaseDAO
from app.orders.models import Orders
from app.database import async_session_maker
from app.shopping_carts.models import ShoppingCarts
from app.users.models import Users


class OrdersDAO(BaseDAO):
    model = Orders

    @classmethod
    async def make_order(cls, user_id):
        async with async_session_maker() as session:
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

            # Удаляем товары из таблицы shopping_carts
            delete_query = delete(ShoppingCarts).where(ShoppingCarts.user_id == user_id)
            await session.execute(delete_query)

            await session.commit()
            await session.refresh(orders_item)
            return orders_item
