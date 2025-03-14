from typing import TYPE_CHECKING

from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.products.models import Products


class Categories(Base):
    __tablename__ = "categories"

    category_name: Mapped[str] = mapped_column(primary_key=True)
