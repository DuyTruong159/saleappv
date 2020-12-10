import json, hashlib
from saleapp import db
from saleapp.models import *

def read_data(path='data/categories.json'):
    with open(path, encoding='utf-8') as f:
        return json.load(f)

def read_product(cat_id = None, kw = None, from_price = None, to_price = None):
    products = Product.query

    if cat_id:
        products = products.filter(Product.category_id == cat_id)

    if kw:
        products = products.filter(Product.name.contains(kw))

    if from_price and to_price:
        products = products.filter(Product.price.__gt__(from_price),
                                   Product.price.__lt__(to_price))

    return products.all()

def get_product_by_id(product_id):
    return Product.query.get(product_id)

def add_user(name, email, username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
    u = User(name=name,
             email=email,
             username=username,
             passwork=password)

    db.session.add(u)
    db.session.commit()

def cart_start(cart):
    quantity, price = 0,0

    for p in cart.values():
        quantity = quantity + p['quantity']
        price = price + p['quantity'] * p['price']

    return quantity, price

def add_receipt(cart):
    if cart:
        try:
            receipt = Receipt(customer_id=1)
            db.session.add(receipt)

            for p in list(cart.values()):
                detail = ReceiptDetail(product_id=int(p["id"]),
                                       receipt_id=receipt.id,
                                       price=float(p["price"]),
                                       quantity=p["quantity"])
                db.session.add(detail)

            db.session.commit()

            return True
        except:
            pass

    return False



