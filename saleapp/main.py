from flask import render_template, request, session, jsonify
from saleapp import app, util, login
from saleapp.models import *
from flask_login import login_user
import hashlib

@app.route("/")
def index():
    categories = util.read_data()
    return render_template('index.html', categories = categories)

@app.route("/products")
def product_list():
    cat_id = request.args.get("cat_id")
    kw = request.args.get("kw")
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    product = util.read_product(cat_id=cat_id, kw=kw, from_price=from_price, to_price=to_price)
    return render_template('products.html', products = product)

@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = util.get_product_by_id(product_id = product_id)
    return render_template('product_detail.html', product = product)

@login.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.route('/login-admin', methods=['get', 'post'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')
        password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())
        user = User.query.filter(User.username == username.strip(),
                                 User.passwork == password).first()

        if user:
            login_user(user=user)

    return redirect("/admin")

@app.route('/register', methods=["get", "post"])
def register():
    err_msg = ''
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')

        if password == confirm:
            if util.add_user(name=name, email=email, username=username, password=password):
                return redirect("/admin")

        else:
            err_msg = 'Mật khẩu không đúng'

    return render_template('register.html', err_msg=err_msg)

@app.route('/api/cart', methods=['get', 'post'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    data = request.json
    id = str(data.get('id'))
    name = data.get('name')
    price = data.get('price')

    if id in cart:
        cart[id]['quantity'] = cart[id]['quantity'] + 1
    else:
        cart[id] = {
            "id": id,
            "name": name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart
    quan, amount = util.cart_start(session['cart'])

    return jsonify({
        "total_quantity": quan,
        "total_amount": amount
    })

@app.route('/payment', methods=['get', 'post'])
def payment():
    if request.method == 'POST':
        if util.add_user(session.get('cart')):
            del session['cart']

            return jsonify({ 'message': 'Payment added!!!' })

    quan, price = util.cart_start(session.get('cart'))

    cart_info = {
        'total_quantity': quan,
        'total_amount': price
    }

    return render_template('payment.html', cart_info=cart_info)

if __name__ == "__main__":
    app.run(debug=True, port=2749)