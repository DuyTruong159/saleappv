from saleapp import admin
from flask_admin.contrib.sqla import ModelView
from flask_admin import BaseView, expose
from saleapp.models import *
from flask_login import current_user
from flask import redirect

class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')

class LogoutView(BaseView):
    @expose('/')
    def index(self):
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated

class RegisterView(BaseView):
    @expose('/')
    def index(self):
        return self.render('/register.html')

admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Product, db.session))
admin.add_view(ContactView(name='Liên hệ'))
admin.add_view(LogoutView(name="Logout"))
admin.add_view(RegisterView(name='Đăng ký'))
