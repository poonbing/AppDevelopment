from flask import Flask, render_template, request, url_for
import shelve
from templates.Product import Product

app = Flask(__name__)


def retrieve_db():
    with shelve.open('products') as db:
        product_list = db['list']
    return product_list


def commit_db(product_list):
    with shelve.open('products') as db:
        db['list'] = product_list
        db.sync()
    return 'Commit successful'

def change_dict(item_class):
    var = {'id': item_class.get_product_id(), 'name': item_class.get_name(),
           'description': item_class.get_description(), 'price': item_class.get_price(),
           'image': item_class.get_image(), 'offer': item_class.get_offer(), "offered": item_class.get_offered_price()}
    return var

def change_class(item_dict):
    var = Product((int(item_dict['id'])-1), item_dict['name'], item_dict['description'], item_dict['price'], item_dict['image'], item_dict['offer'])
    return var

product_id = '1'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        product_list = retrieve_db()
        product = product_list[product_id]
        product['name'] = request.form['name']
        product['price'] = f"{float(request.form['price']):.2f}"
        product['description'] = request.form['description']
        product['offer'] = request.form['offer']
        product_list[product_id] = product
        print(product)
        commit_db(product_list)
        products = [change_class(product)]
        return render_template('product-index.html', products=products)
    else:
        product_list = retrieve_db()
        product = product_list[product_id]
        print(product)
        products = [change_class(product)]
        return render_template("product-index.html", products=products)


if __name__ == '__main__':
    app.run(debug=True)
