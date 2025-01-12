from app.dao.base import BaseDAO
from app.products.models import Products


class ProductDAO(BaseDAO):
    model = Products
