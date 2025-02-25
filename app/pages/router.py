from fastapi import APIRouter, Depends
from fastapi.templating import Jinja2Templates
from fastapi import Request
from fastapi.responses import HTMLResponse

from app.products.dao import ProductDAO
from app.products.router import get_products
from app.reviews.dao import ReviewsDAO
from app.shopping_carts.dao import CartsDAO
from app.users.dependencies import get_current_user
from app.users.models import Users

router = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")


@router.get("/login", response_class=HTMLResponse)
async def get_login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def get_register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.get("/products")
async def get_product_page(
        request: Request,
        products=Depends(get_products)
):
    return templates.TemplateResponse(
        name="products.html",
        context={"request": request, "products": products}
    )


@router.get("/cart")
async def get_cart_page(request: Request, user: Users = Depends(get_current_user)):
    cart_items = await CartsDAO.get_cart_items(user.id)
    return templates.TemplateResponse("cart.html", {"request": request, "cart_items": cart_items})


@router.get("/product/{product_id}")
async def get_product_detail_page(request: Request, product_id: int):
    product = await ProductDAO.get_product_by_id(product_id)
    reviews = await ReviewsDAO.get_reviews_by_product_id(product_id)
    return templates.TemplateResponse("product_detail.html", {
        "request": request,
        "product": product,
        "reviews": reviews
    })