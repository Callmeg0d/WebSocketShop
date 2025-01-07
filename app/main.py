from fastapi import FastAPI


app = FastAPI()


@app.get("/product/{product_name}")
async def root(product_name: str):
    return product_name
