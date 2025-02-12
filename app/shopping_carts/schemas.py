from pydantic import BaseModel, ConfigDict


class SShoppingCart(BaseModel):
    product_id: int
    quantity: int

    model_config = ConfigDict(from_attributes=True)