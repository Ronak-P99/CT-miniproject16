from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class Product(Base):
    __tablename__ = 'Products'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    price: Mapped[float] = mapped_column(db.Float, nullable=False)
    quantity_ordered: Mapped[int] = mapped_column(nullable=False)
    order_id: Mapped[int] = mapped_column(db.ForeignKey('Orders.id'))

    production: Mapped["Production"] = db.relationship(back_populates="product")
    order: Mapped["Order"] = db.relationship(back_populates="product")