from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


class Reviews(Base):
    __tablename__ = "reviews"

    review_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))
    feedback: Mapped[str] = mapped_column()
    rating: Mapped[int] = mapped_column(nullable=False)


    user: Mapped["Users"] = relationship(back_populates="reviews")
    product: Mapped["Products"] = relationship(back_populates="reviews")