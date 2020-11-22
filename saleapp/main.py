from flask import render_template
from saleapp import app, util, login
from saleapp.models import *
from flask import redirect, request
from flask_login import login_user
import hashlib, os

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
            avatar = request.files['avatar']
            avatar_path = 'images/uploads/&s' % avatar.filename
            avatar.save(os.path.join(app.config['ROOT_PROJECT_PATH'], 'static/', avatar_path ))

            if util.add_user(name=name, email=email, username=username, password=password, avatar=avatar_path):
                return redirect('/admin')

        else:
            err_msg = 'Mật khẩu không đúng'

    return render_template('register.html', err_msg=err_msg)

if __name__ == "__main__":
    app.run(debug=True)

