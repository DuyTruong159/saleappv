from flask import render_template
from saleapp import app, util

@app.route("/")
def index():
    categories = util.read_data()
    return render_template('index.html', categories = categories)

@app.route("/products")
def product_list():
    product = util.read_data(path='data/products.json')
    return render_template('products.html', products = product)

@app.route("/products/<int:product_id>")
def product_detail(product_id):
    product = util.get_product_by_id(product_id = product_id)
    return render_template('product_detail.html', product = product)

if __name__ == "__main__":
    app.run(debug=True)

