from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict


class SOrderResponse(BaseModel):
    order_id: int
    user_id: int
    created_at: datetime
    status: str
    delivery_address: str
    order_items: List[Dict[str, int]]
    total_cost: int

    class Config:
        from_attributes = True
