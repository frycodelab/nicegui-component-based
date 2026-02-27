from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class Order(Base):

    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    customer_name: Mapped[str] = mapped_column(
        String(100)
    )

    product: Mapped[str] = mapped_column(
        String(100)
    )

    quantity: Mapped[int] = mapped_column(
        Integer
    )