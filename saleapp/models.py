from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean,Date, Enum
from sqlalchemy.orm import relationship
from saleapp import db
from datetime import datetime
from enum import Enum as UserEnum
from flask_login import UserMixin

class SaleBass(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

    def __str__(self):
        return self.name

class Category(SaleBass):
    __tablename__ = 'category'

    products = relationship('Product', backref = 'category', lazy = True)

class Product(SaleBass):
    __tablename__ = 'product'

    desciption = Column(String(255))
    price = Column(Float, default=0)
    image = Column(String(255))
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)

class UserRole(UserEnum):
    USER = 1
    ADMIN = 2

class User(SaleBass, UserMixin):
    __tablename__ = 'user'

    email = Column(String(50))
    username = Column(String(100), nullable=False)
    passwork = Column(String(100), nullable=False)
    avarter = Column(String(100))
    acitive = Column(Boolean, default=True)
    joined_date = Column(Date, default=datetime.now())
    user_role = Column(Enum(UserRole, default=UserRole.USER))

if __name__ == '__main__':
    db.create_all()

