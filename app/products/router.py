from fastapi import APIRouter
from app.products.dao import ProductDAO
from app.products.schemas import SProducts

router = APIRouter(
    prefix="/products",
    tags=["Товары"]
)


@router.get("")
async def get_products() -> list[SProducts]:
    return await ProductDAO.find_all()
