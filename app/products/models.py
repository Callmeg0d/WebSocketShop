from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import JSON, ForeignKey


class Products(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[int] = mapped_column(nullable=False)
    product_quantity: Mapped[int] = mapped_column(nullable=False)
    image: Mapped[int] = mapped_column(nullable=False)
    features: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    category_name: Mapped[str] = mapped_column(ForeignKey("categories.category_name"))


    category: Mapped["Categories"] = relationship(back_populates="products")
    carts: Mapped[list["ShoppingCarts"]] = relationship(back_populates="product")
    reviews: Mapped[list["Reviews"]] = relationship(back_populates="product")