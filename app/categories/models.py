from app.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Categories(Base):
    __tablename__ = "categories"

    category_name: Mapped[str] = mapped_column(primary_key=True)

    products: Mapped[list["Products"]] = relationship( back_populates="category")
