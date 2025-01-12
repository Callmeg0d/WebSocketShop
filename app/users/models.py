from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.shopping_carts.models import ShoppingCarts
from app.reviews.models import Reviews
from app.orders.models import Orders


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column()
    hashed_password: Mapped[str] = mapped_column()
    delivery_address: Mapped[str] = mapped_column()

    carts: Mapped["ShoppingCarts"] = relationship(back_populates="user")
    reviews: Mapped[list["Reviews"]] = relationship(back_populates="user")
    orders: Mapped[list["Orders"]] = relationship(back_populates="user")

    def __str__(self):
        return f"User {self.email}"

