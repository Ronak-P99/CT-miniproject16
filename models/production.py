from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
import datetime

class Production(Base):
    __tablename__ = 'Productions'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    quantity_produced: Mapped[int] = mapped_column(nullable=False)
    product_id: Mapped[int] = mapped_column(db.ForeignKey('Products.id'))
    employee_id: Mapped[int] = mapped_column(db.ForeignKey('Employees.id'))
    date: Mapped[datetime.date] = mapped_column(db.Date, nullable=False)
    
    product: Mapped["Product"] = db.relationship(back_populates="production")
    employee: Mapped["Employee"] = db.relationship(back_populates="production")