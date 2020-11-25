from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager

app = Flask(__name__)

app.secret_key="*C\x01\xc1\xc6\xb5W\xed\xccV#\xa3\xf2v%\x04"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:phamduytruong@localhost/saledbv1?charset=utf8'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app=app)
admin = Admin(app=app, name="IT81 SHOP", template_mode="bootstrap4")
login = LoginManager(app=app)
