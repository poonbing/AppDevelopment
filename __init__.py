from flask import Flask, render_template, request, url_for, redirect
import shelve
from Forms import CreateNewProductForm
from Decks import Deck
import random

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


print(retrieve_db('products', 'decks'))


# --Lewis--:Homepage
@app.route("/")
def homepage():
    db = retrieve_db('products', 'decks')
    data = list(db.values())
    topitems = []
    items = random.sample(data, k=8)
    for product in items:
        topitems.append(Deck((int(product['id'])-1), product['name'], product['brand'], product['type'], product['description'], product['price'], product['image'], product['offer']))
    newitems = []
    data.reverse()
    for c in range(0, 8):
        product = data[c]
        newitems.append(Deck((int(product['id'])-1), product['name'], product['brand'], product['type'], product['description'], product['price'], product['image'], product['offer']))

    return render_template('home.html', top_items=topitems, new_items=newitems)


@app.route("/accessories")
def homepage_accessories():
    return render_template('accessories.html')


@app.route('/luxuryDecks', methods=['GET', 'POST'])
def create_new_luxury():
    create_product_form = CreateNewProductForm(request.form)
    if request.method == 'POST' and create_product_form.validate():
        product = {
            'id': current_count('products', 'decks'),
            'name': create_product_form.name.data,
            'brand': create_product_form.brand.data,
            'type': 'Luxury',
            'description': create_product_form.description.data,
            'price': f"{create_product_form.price.data:.2f}",
            'image': create_product_form.image.data,
            'offer': 0
        }
        with shelve.open('products') as db:
            decks = db['decks']
            decks.append(product)
            db['decks'] = decks
            db.sync()
        luxury_decks = Deck((int(product['id'])-1), product['name'], product['brand'], product['type'], product['description'], product['price'], product['image'], product['offer'])
        print(product, 'is stored in luxurydecks.db successfully with Product ID == ', luxury_decks.get_product_id())
    return render_template('luxuryDecks.html', form=create_product_form)


@app.route('/retrieveluxuryDecks', methods=['GET', 'POST'])
def retrieve_luxury():
    db = retrieve_db('products', 'decks')
    data = list(db.values())
    products = []
    for product in data:
        if product['type'] == "Luxury":
            products.append(Deck((int(product['id'])-1), product['name'], product['brand'], product['type'], product['description'], product['price'], product['image'], product['offer']))
        else:
            pass
    return render_template('retrieveluxuryDecks.html', products=products)


@app.route('/classicDecks', methods=['GET', 'POST'])
def create_new_classic():
    create_product_form = CreateNewProductForm(request.form)
    if request.method == 'POST' and create_product_form.validate():
        product = {
            'id': current_count('products', 'decks'),
            'name': create_product_form.name.data,
            'brand': create_product_form.brand.data,
            'type': 'Classic',
            'description': create_product_form.description.data,
            'price': f"{create_product_form.price.data:.2f}",
            'image': create_product_form.image.data,
            'offer': 0
        }
        with shelve.open('products') as db:
            decks = db['decks']
            decks.append(product)
            db['decks'] = decks
            db.sync()
        luxury_decks = Deck((int(product['id'])-1), product['name'], product['brand'], product['type'], product['description'], product['price'], product['image'], product['offer'])
        print(product, 'is stored in luxurydecks.db successfully with Product ID == ', luxury_decks.get_product_id())
    return render_template('classicDecks.html', form=create_product_form)


@app.route('/retrieveclassicDecks', methods=['GET', 'POST'])
def retrieve_classic():
    db = retrieve_db('products', 'decks')
    data = list(db.values())
    products = []
    for product in data:
        if product['type'] == "Classic":
            products.append(Deck((int(product['id'])-1), product['name'], product['brand'], product['type'], product['description'], product['price'], product['image'], product['offer']))
        else:
            pass
    return render_template('retrieveclassicDecks.html', products=products)


@app.route('/cardistryDecks', methods = ['GET', 'POST'])
def create_new_cardistry():
    create_product_form = CreateNewProductForm(request.form)
    if request.method == 'POST' and create_product_form.validate():
        product = {
            'id': current_count('products', 'decks'),
            'name': create_product_form.name.data,
            'brand': create_product_form.brand.data,
            'type': 'Cardistry',
            'description': create_product_form.description.data,
            'price': f"{create_product_form.price.data:.2f}",
            'image': create_product_form.image.data,
            'offer': 0
        }
        with shelve.open('products') as db:
            decks = db['decks']
            decks.append(product)
            db['decks'] = decks
            db.sync()
        luxury_decks = Deck((int(product['id'])-1), product['name'], product['brand'], product['type'], product['description'], product['price'], product['image'], product['offer'])
        print(product, 'is stored in luxurydecks.db successfully with Product ID == ', luxury_decks.get_product_id())
    return render_template('cardistryDecks.html', form=create_product_form)


@app.route('/retrievecardistryDecks', methods=['GET', 'POST'])
def retrieve_cardistry():
    db = retrieve_db('products', 'decks')
    data = list(db.values())
    products = []
    for product in data:
        if product['type'] == "Cardistry":
            products.append(Deck((int(product['id'])-1), product['name'], product['brand'], product['type'], product['description'], product['price'], product['image'], product['offer']))
        else:
            pass
    return render_template('retrievecardistryDecks.html', products=products)
# --Lewis--:Homepage end


# --BP--:Product view start
@app.route('/product', methods=['POST', 'GET'])
def product_page():
    product_list = retrieve_db('products', 'decks')
    product_id = '1'
    product = product_list[product_id]
    products = [Deck((int(product['id'])-1), product['name'], product['brand'], product['type'], product['description'], product['price'], product['image'], product['offer'])]
    return render_template("product-index.html", products=products)


@app.route('/update', methods=['POST', 'GET'])
def update_product_info():
    product_id = request.form.get('submit')
    if request.method == 'POST':
        product_list = retrieve_db('products', 'decks')
        product_id = '1'
        product = product_list[product_id]
        if request.form['name'] != "":
            product['name'] = request.form['name']
        if request.form['brand'] != "":
            product['brand'] = request.form['brand']
        if request.form['type'] != "":
            product['type'] = request.form['type']
        if request.form['price'] != "":
            product['price'] = f"{float(request.form['price']):.2f}"
        if request.form['description'] != "":
            product['description'] = request.form['description']
        if request.form['offer'] != "":
            product['offer'] = request.form['offer']
        if request.form['image'] != "":
            product.form['image'] = request.form['image']
        product_list[product_id] = product
        commit_db('products', 'decks', product_list)
        print('updated')
        return redirect(url_for('product_page'))
    else:
        print('updating')
        return render_template('update.html')


@app.route('/create', methods=['POST', 'GET'])
def create_new_product():
    if request.method == 'POST':
        product_list = retrieve_db('products', 'decks')
        new_id = current_count('products', 'decks')
        product = {}
        product['id'] = str(new_id)
        product['name'] = request.form['name']
        product['brand'] = request.form['brand']
        product['type'] = request.form['type']
        product['price'] = f"{float(request.form['price']):.2f}"
        product['description'] = request.form['description']
        product['image'] = request.form['image']
        product['offer'] = request.form['offer']
        product_list[new_id] = product
        commit_db('products', 'decks', product_list)
        print('item created')
        return redirect(url_for('product_page'))
    else:
        print('creating item')
        return render_template('create.html')


@app.route('/delete', methods=['POST', 'GET'])
def delete():
    if request.method == "POST":
        delete_id = request.form.get('submit')
        product = retrieve_db('products', 'decks')
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
        commit_db('products', 'decks', product_list)
        product_list = product_list.values()
        return render_template('delete.html', product_list=product_list)
    else:
        product_list = retrieve_db('products', 'decks')
        product_list = product_list.values()
        return render_template('delete.html', product_list=product_list)
# --BP--:Product view end


if __name__ == '__main__':
    app.run(debug=True)
