from fastapi import FastAPI
from app.products.router import router as router_products
from app.users.router import router as router_users
from app.orders.router import router as router_orders
from app.shopping_carts.router import router as shopping_carts_orders

app = FastAPI()

app.include_router(router_users)
app.include_router(router_products)
app.include_router(router_orders)
app.include_router(shopping_carts_orders)




