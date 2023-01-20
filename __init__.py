from flask import Flask, render_template, request, url_for, redirect
import shelve
from templates.Product import Product

app = Flask(__name__)


def retrieve_db(shelve_name, key):
    with shelve.open(shelve_name) as db:
        output = db[key]
    return output


def commit_db(shelve_name, key, new_list):
    with shelve.open(shelve_name) as db:
        db[key] = new_list
        db.sync()
    return 'Commit successful'

def current_count(shelve_name, key):
    db = retrieve_db(shelve_name, key)
    count = 1
    for keys in db:
        count += 1
    counter = str(count)
    return counter

def change_dict(item_class):
    var = {'id': item_class.get_product_id(), 'name': item_class.get_name(),
           'description': item_class.get_description(), 'price': item_class.get_price(),
           'image': item_class.get_image(), 'offer': item_class.get_offer(), "offered": item_class.get_offered_price()}
    return var

def change_class(item_dict):
    var = Product((int(item_dict['id'])-1), item_dict['name'], item_dict['description'], item_dict['price'], item_dict['image'], item_dict['offer'])
    return var

product_id = '1'
product = {
    '1': {
        'id': '1', 'name': 'amogus', 'description': 'AMONG US 3AM POTION', 'price': 1000, 'image': 'cirno.jpg', 'offer': 10},
    '2': {
        'id': '2', 'name': 'Your mom', 'price': '0.00', 'description': 'Yes. Your mom.', 'image': 'mom.jpg', 'offer': '0'}, '3': {'id': '3', 'name': 'JOBAMAAA', 'price': '1.00', 'description': 'obama but joker', 'image': 'obama.jpg', 'offer': '0'}, '4': {'id': '4', 'name': "CLAIRE'S MOM", 'price': '0.00', 'description': 'CLAIREEEEEEEEEEEEEE', 'image': 'claire.jpg', 'offer': '0'}, '5': {'id': '5', 'name': 'Cherry', 'price': '100.00', 'description': 'God this sucks', 'image': 'files', 'offer': '0'}}
commit_db('products', 'list', product)

@app.route('/', methods=['POST', 'GET'])
def index():
    product_list = retrieve_db('products', 'list')
    product = product_list[product_id]
    products = [change_class(product)]
    return render_template("product-index.html", products=products)

@app.route('/update.html', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        product_list = retrieve_db('products', 'list')
        print(product_list)
        product = product_list[product_id]
        if request.form['name'] != "":
            product['name'] = request.form['name']
        if request.form['price'] != "":
            product['price'] = f"{float(request.form['price']):.2f}"
        if request.form['description'] != "":
            product['description'] = request.form['description']
        if request.form['offer'] != "":
            product['offer'] = request.form['offer']
        if request.form['image'] != "":
            product.form['image'] = request.form['image']
        product_list[product_id] = product
        print(product_list)
        commit_db('products', 'list', product_list)
        print('updated')
        return redirect(url_for('index'))
    else:
        print('updating')
        return render_template('update.html')

@app.route('/create.html', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        product_list = retrieve_db('products', 'list')
        print(product_list)
        new_id = current_count('products', 'list')
        print(new_id)
        product = {}
        product['id'] = str(new_id)
        product['name'] = request.form['name']
        product['price'] = f"{float(request.form['price']):.2f}"
        product['description'] = request.form['description']
        product['image'] = request.form['image']
        product['offer'] = request.form['offer']
        product_list[new_id] = product
        print(product_list)
        commit_db('products', 'list', product_list)
        print('item created')
        return redirect(url_for('index'))
    else:
        print('creating item')
        return render_template('create.html')

@app.route('/delete.html', methods=['POST', 'GET'])
def delete():
    if request.method == "POST":
        delete_id = request.form.get('submit')
        product = retrieve_db('products', 'list')
        cid = str(delete_id)
        product.pop(cid)
        count = 1
        product_list = {}
        for keys in product:
            cid = str(count)
            item = product[keys]
            item['id'] = cid
            product_list[cid] = item
            count += 1
        commit_db('products', 'list', product_list)
        product_list = product_list.values()
        return render_template('delete.html', product_list=product_list)
    else:
        product_list = retrieve_db('products', 'list')
        product_list = product_list.values()
        return render_template('delete.html', product_list=product_list)

if __name__ == '__main__':
    app.run(debug=True)
