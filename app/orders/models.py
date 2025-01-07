from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Date, JSON
from datetime import date


class Orders(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    delivery_address: Mapped[str] = mapped_column(nullable=False)
    order_items: Mapped[list[str]] = mapped_column(JSON, nullable=False)
    total_cost: Mapped[int] = mapped_column(nullable=False)


    user: Mapped["Users"] = relationship(back_populates="orders")
