from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi import Request

from app.products.router import get_products

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/products")
async def get_product_page(
        request: Request,
        products=Depends(get_products)
):
    return templates.TemplateResponse(
        name="products.html",
        context={"request": request, "products": products}
    )
