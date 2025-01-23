from typing import TYPE_CHECKING

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

if TYPE_CHECKING:
    from app.users.models import Users
    from app.products.models import Products


class ShoppingCarts(Base):
    __tablename__ = "shopping_carts"

    cart_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    quantity: Mapped[int] = mapped_column()
    total_cost: Mapped[int] = mapped_column()

    user: Mapped["Users"] = relationship("Users", back_populates="shopping_carts")
    product: Mapped["Products"] = relationship("Products", back_populates="shopping_carts")
