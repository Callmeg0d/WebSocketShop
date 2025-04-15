from sqlalchemy import select

from app.dao.base import BaseDAO
from app.database import async_session_maker
from app.products.models import Products


class ProductDAO(BaseDAO):
    model = Products

    @classmethod
    async def get_product_by_id(cls, product_id):
        async with async_session_maker() as session:
            query = select(
                Products.product_id,
                Products.name,
                Products.description,
                Products.price,
                Products.product_quantity,
                Products.image,
                Products.features,
                Products.category_name,
            ).where(Products.product_id == product_id)
            result = await session.execute(query)
            return result.mappings().first()
