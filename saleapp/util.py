import json, hashlib
from saleapp import db
from saleapp.models import User

def read_data(path='data/categories.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def read_product(cat_id = None, kw = None, from_price = None, to_price = None):
    products = read_data(path='data/products.json')

    if cat_id:
        cat_id = int(cat_id)
        products = [p for p in products if (p['category_id'] == cat_id)]
    if kw:
        products = [p for p in products if p['name'].find(kw) >= 0]
    if from_price and to_price:
        from_price = float(from_price)
        to_price = float(to_price)
        products = [p for p in products if p['price'] >= from_price and p['price'] <= to_price]

    return products

def get_product_by_id(product_id):
    products = read_data('data/products.json')
    for p in products:
        if p["id"] == product_id:
            return p

def add_user(name, email, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name,
             email=email,
             username=username,
             passwork=password)

    db.session.add(u)
    db.session.commit()
