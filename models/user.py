from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from typing import List


class User(Base):
    __tablename__ = 'Users'
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(255), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(320), nullable=False)
    roles: Mapped[List["Role"]] = db.relationship(secondary="Customer_Management_Roles")
