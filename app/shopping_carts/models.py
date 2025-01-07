from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class ShoppingCarts(Base):
    __tablename__ = "shopping_carts"

    cart_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    quantity: Mapped[int] = mapped_column(nullable=False)
    total_cost: Mapped[int] = mapped_column(nullable=False)


    user: Mapped["Users"] = relationship(back_populates="shopping_carts")
    product: Mapped["Products"] = relationship(back_populates="shopping_carts")