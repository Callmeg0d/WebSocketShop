from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.products.models import Products


class Categories(Base):
    __tablename__ = "categories"

    category_name: Mapped[str] = mapped_column(primary_key=True)
