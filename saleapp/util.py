import json, hashlib
from saleapp import db
from saleapp.models import User

def read_data(path='data/categories.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def get_product_by_id(product_id):
    products = read_data('data/products.json')
    for p in products:
        if p["id"] == product_id:
            return p

def add_user(name, email, username, password, avatar):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name,
             email=email,
             username=username,
             password=password,
             avatar=avatar)

    db.session.add(u)
    db.session.commit()
