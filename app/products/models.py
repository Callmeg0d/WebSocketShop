from typing import Optional, TYPE_CHECKING

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, ForeignKey

if TYPE_CHECKING:
    from app.shopping_carts.models import ShoppingCarts
    from app.reviews.models import Reviews


class Products(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    price: Mapped[int] = mapped_column()
    product_quantity: Mapped[int] = mapped_column()
    image: Mapped[Optional[int]]
    features: Mapped[Optional[list[str]]] = mapped_column(JSON)
    category_name: Mapped[str] = mapped_column(ForeignKey("categories.category_name"))

    shopping_carts: Mapped[list["ShoppingCarts"]] = relationship(back_populates="product")
    reviews: Mapped[list["Reviews"]] = relationship("Reviews", back_populates="product")
