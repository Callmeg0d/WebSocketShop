from fastapi import FastAPI
from app.products.router import router as router_products
from app.users.router import router_auth as router_users
from app.orders.router import router as router_orders
from app.shopping_carts.router import router as router_shopping_carts
from app.pages.router import router as router_pages
from app.images.router import router as router_images
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), "static")

app.include_router(router_users)
app.include_router(router_products)
app.include_router(router_orders)
app.include_router(router_shopping_carts)
app.include_router(router_pages)
app.include_router(router_images)

# Подключение CORS, чтобы запросы к API могли приходить из браузера
origins = [
    "http://127.0.0.1:8000",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)
