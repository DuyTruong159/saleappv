from sqlalchemy import Column, Integer, Float, String, ForeignKey, Boolean,Date, Enum, DateTime
from sqlalchemy.orm import relationship
from saleapp import db, admin
from datetime import datetime
from enum import Enum as UserEnum
from flask import redirect
from flask_login import UserMixin, current_user, logout_user
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView

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
    receipt_detail = relationship('ReceiptDetail', backref='product', lazy=True)

class UserRole(UserEnum):
    USER = 1
    ADMIN = 2

class User(SaleBass, UserMixin):
    __tablename__ = 'user'

    email = Column(String(50))
    username = Column(String(100), nullable=False)
    passwork = Column(String(100), nullable=False)
    acitive = Column(Boolean, default=True)
    joined_date = Column(Date, default=datetime.now())
    user_role = Column(Enum(UserRole, default=UserRole.USER))
    receipts = relationship('Receipt', backref='user', lazy=True)

class Receipt(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    created_date = Column(DateTime, default=datetime.today())
    customer_id = Column(Integer, ForeignKey(User.id))
    receipt_detail = relationship('ReceiptDetail', backref='receipt', lazy=True)

class ReceiptDetail(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey(Product.id))
    receipt_id = Column(Integer, ForeignKey(Receipt.id))
    quantity = Column(Integer, default=0)
    price = Column(Float, default=0)

class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class RegisterView(BaseView):
    @expose('/')
    def index(self):
        return self.render('/register.html')

class CategoryModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

class ProductModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

admin.add_view(CategoryModelView(Category, db.session))
admin.add_view(ProductModelView(Product, db.session))
admin.add_view(ContactView(name='Liên hệ'))
admin.add_view(LogoutView(name="Logout"))
admin.add_view(RegisterView(name='Đăng ký'))

if __name__ == '__main__':
    db.create_all()

