from flask import Flask, render_template, request, url_for, redirect
import shelve
from Form1 import CreateDeckForm
from Form2 import UpdateDeckForm
from Form3 import CreateTutorial, CreateAccessories
from Decks import Deck
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SecretKey'


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


def unique_id(type):
    idc = str(random.randint(100, 999))
    if type == 'decks':
        kind = 'D'
        db = retrieve_db('products', 'decks')
        keys = db.keys()
        output = kind+idc
        if output in keys:
            return unique_id(type)
        else:
            return output
    elif type == 'accessories':
        kind = 'A'
        db = retrieve_db('products', 'accessories')
        keys = db.keys()
        output = kind+idc
        if output in keys:
            return unique_id(type)
        else:
            return output
    elif type == 'user':
        kind = 'U'
        db = retrieve_db('users', 'users')
        keys = db.keys()
        output = kind+idc
        if output in keys:
            return unique_id(type)
        else:
            return output


def generate_receipt():
    idc = str(random.randint(100000, 999999))
    return idc


def offered_price(price, offer):
    of = float(float(price)*((100 - int(offer)) / 100))
    offer_price = f"{of:.2f}"
    return offer_price


# --Lewis--:Homepage
@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        product_list = retrieve_db('products', 'decks')
        product_id = request.form.get("id")
        print(product_id)
        product = [product_list[product_id]]
        print(product)
        return render_template("product-index.html", products=product)
    else:
        db = retrieve_db('products', 'decks')
        data = list(db.values())
        topitems = []
        items = random.sample(data, k=8)
        for product in items:
            topitems.append(product)
        newitems = []
        data.reverse()
        for c in range(0, 8):
            product = data[c]
            newitems.append(product)
        return render_template('home.html', top_items=topitems, new_items=newitems)


@app.route('/luxuryDecks', methods=['GET', 'POST'])
def product_database():
    form = CreateDeckForm(request.form)
    form2 = UpdateDeckForm(request.form)
    if request.method == 'POST':
        if request.form.get('submit') == 'create':
            product = {
                'id': current_count('products', 'decks'),
                'name': form.name.data,
                'brand': form.brand.data,
                'type': form.type.data,
                'description': form.description.data,
                'price': f"{form.price.data:.2f}",
                'image': form.picture.data,
                'offer': form.offer.data,
                'offered price': offered_price(form.price.data, form.offer.data)
            }
            with shelve.open('products') as db:
                decks = db['decks']
                decks[current_count('products', 'decks')] = product
                db['decks'] = decks
                db.sync()
            print('created')
            return redirect(url_for('product_database'))
        elif request.form.get('submit') in retrieve_db('products', 'decks'):
            print(request.form.get('submit'))
            if request.form.get('function') == "delete":
                delete_id = request.form.get('submit')
                print(delete_id)
                product = retrieve_db('products', 'decks')
                cid = str(delete_id)
                product.pop(cid)
                count = 0
                product_list = {}
                for keys in product:
                    count += 1
                    cid = str(count)
                    item = product[keys]
                    item['id'] = cid
                    product_list[cid] = item
                commit_db('products', 'decks', product_list)
                print("deleted")
                return redirect(url_for('product_database'))
        elif request.form.get('function') == 'update':
            print('clear 1')
            db = retrieve_db('products', 'decks')
            uid = request.form.get('product_id')
            print(uid)
            product = db[uid]
            if form2.name.data != "":
                product['name'] = form2.name.data
                print('name')
            if form2.brand.data != "":
                product['brand'] = form2.brand.data
            if form2.type.data is not None:
                product['type'] = form2.type.data
            if form2.description.data != "":
                product['description'] = form2.description.data
            if form2.price.data is not None:
                product['price'] = f"{form2.price.data:.2f}"
            if form2.picture.data != "":
                product['image'] = form2.picture.data
            if form2.offer.data is not None:
                print('offer change')
                product['offer'] = form2.offer.data
                product['offered price'] = offered_price(product['price'], product['offer'])
            uid = str(uid)
            db[uid] = product
            commit_db('products', 'decks', db)
            print("updated")
            return redirect(url_for('product_database'))
    else:
        product = retrieve_db('products', 'decks')
        product_list = product.values()
        return render_template('luxuryDecks.html', form=form, form2=form2, product_list=product_list, product=product)


@app.route('/retrieveluxuryDecks', methods=['GET', 'POST'])
def retrieve_luxury():
    if request.method == 'POST':
        product_list = retrieve_db('products', 'decks')
        product_id = request.form.get("id")
        print(product_id)
        product = [product_list[product_id]]
        print(product)
        return render_template("product-index.html", products=product)
    else:
        db = retrieve_db('products', 'decks')
        data = list(db.values())
        products = []
        for product in data:
            if product['type'] == "Luxury":
                products.append(product)
            else:
                pass
        return render_template('retrieveluxuryDecks.html', products=products)


@app.route('/retrieveclassicDecks', methods=['GET', 'POST'])
def retrieve_classic():
    if request.method == 'POST':
        product_list = retrieve_db('products', 'decks')
        product_id = request.form.get("id")
        print(product_id)
        product = [product_list[product_id]]
        print(product)
        return render_template("product-index.html", products=product)
    else:
        db = retrieve_db('products', 'decks')
        data = list(db.values())
        products = []
        for product in data:
            if product['type'] == "Classic":
                products.append(product)
            else:
                pass
        return render_template('retrieveclassicDecks.html', products=products)


@app.route('/retrievecardistryDecks', methods=['GET', 'POST'])
def retrieve_cardistry():
    if request.method == 'POST':
        product_list = retrieve_db('products', 'decks')
        product_id = request.form.get("id")
        print(product_id)
        product = [product_list[product_id]]
        print(product)
        return render_template("product-index.html", products=product)
    else:
        db = retrieve_db('products', 'decks')
        data = list(db.values())
        products = []
        for product in data:
            if product['type'] == "Cardistry":
                products.append(product)
            else:
                pass
        return render_template('retrievecardistryDecks.html', products=products)
# --Lewis--:Homepage end


# --BP--:Product view start
@app.route('/product', methods=['POST', 'GET'])
def product_page():
    if request.method == 'GET':
        product_list = retrieve_db('products', 'decks')
        product_id = request.form['id']
        product = product_list[product_id]
        products = [Deck((int(product['id'])-1), product['name'], product['brand'], product['type'], product['description'], product['price'], product['image'], product['offer'])]
        return render_template("product-index.html", products=products)
    if request.method == "POST":
        select_id = request.form.get('select id')
        quantity = request.form.get('quantity')
        db = retrieve_db('user', 'cart')
        if select_id in db:
            existing = db[select_id]
            quantity = int(existing)+int(quantity)
            db[select_id] = int(quantity)
            print(db)
            commit_db('user', 'cart', db)
        elif select_id not in db:
            db[select_id] = int(quantity)
            print(db)
            commit_db('user', 'cart', db)
        product_list = retrieve_db('products', 'decks')
        products = [product_list[select_id]]
        return render_template("product-index.html", products=products)


@app.route('/update', methods=['POST', 'GET'])
def update_product_info():
    product_id = request.form.get('submit')
    print(product_id)
    if request.method == 'POST':
        product_list = retrieve_db('products', 'decks')
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
            product['offered price'] = offered_price(product['price'], product['offer'])
        if request.form['image'] != "":
            product.form['image'] = request.form['image']
        product_list[product_id] = product
        commit_db('products', 'decks', product_list)
        print('updated')
        return redirect(url_for('homepage'))
    else:
        print('updating')
        return render_template('update.html')
# --BP--:Product view end


@app.route('/createAccessories', methods=['POST', 'GET'])
def create_accessories():
    form = CreateAccessories(request.form)
    if request.method == 'POST':
        if request.form.get('submit') == 'create':
            product = {
                'id': current_count('products', 'accessories'),
                'name': form.name.data,
                'brand': form.brand.data,
                'description': form.description.data,
                'price': f"{form.price.data:.2f}",
                'image': form.picture.data,
                'offer': form.offer.data,
                'offered price': offered_price(form.price.data, form.offer.data)
            }
            db = retrieve_db('products', 'accessories')
            db[current_count('products', 'accessories')] = product
            commit_db('Accessories', 'accessories', db)
            print('created')
            return redirect(url_for('create_accessories'))
        elif request.form.get('submit') in retrieve_db('products', 'accessories'):
            print(request.form.get('submit'))
            if request.form.get('function') == "delete":
                delete_id = request.form.get('submit')
                print(delete_id)
                product = retrieve_db('products', 'accessories')
                cid = str(delete_id)
                product.pop(cid)
                count = 0
                product_list = {}
                for keys in product:
                    count += 1
                    cid = str(count)
                    item = product[keys]
                    item['id'] = cid
                    product_list[cid] = item
                commit_db('products', 'accessories', product_list)
                print("deleted")
                return redirect(url_for('create_accessories'))
    else:
        product = retrieve_db('Accessories', 'accessories')
        product_list = product.values()
        return render_template('CreateAccessories.html', form=form, product_list=product_list, product=product)


@app.route('/accessories', methods=['GET', 'POST'])
def retrieve_accessories():
        if request.method == 'POST':
            product_list = retrieve_db('products', 'accessories')
            product_id = request.form.get("id")
            print(product_id)
            product = [product_list[product_id]]
            print(product)
            return render_template("product-index.html", products=product)
        else:
            db = retrieve_db('products', 'accessories')
            data = list(db.values())
            products = []
            for product in data:
                products.append(product)

        return render_template('accessories.html', products=products)


@app.route('/createTutorial', methods=['POST', 'GET'])
def create_tutorial():
    form = CreateTutorial(request.form)
    if request.method == 'POST':
        if request.form.get('submit') == 'create':
            video = {
                'id': current_count('Tutorial', 'video'),
                'name': form.name.data,
                'difficulty': form.difficulty.data,
                'type': form.type.data,
                'video': form.video.data,
                'thumbnail': form.thumbnail.data,
            }
            db = retrieve_db('Tutorial', 'video')
            db[current_count('Tutorial', 'video')] = video
            commit_db('Tutorial', 'video', db)
            print('created')
            return redirect(url_for('create_tutorial'))
        elif request.form.get('submit') in retrieve_db('Tutorial', 'video'):
            print(request.form.get('submit'))
            if request.form.get('function') == "delete":
                delete_id = request.form.get('submit')
                print(delete_id)
                product = retrieve_db('Tutorial', 'video')
                cid = str(delete_id)
                product.pop(cid)
                count = 0
                product_list = {}
                for keys in product:
                    count += 1
                    cid = str(count)
                    item = product[keys]
                    item['id'] = cid
                    product_list[cid] = item
                commit_db('Tutorial', 'video', product_list)
                print("deleted")
                return redirect(url_for('create_tutorial'))
    else:
        video = retrieve_db('Tutorial', 'video')
        tutorial_list = video.values()
        return render_template('createTutorial.html', form=form, tutorial_list=tutorial_list, video=video)


@app.route('/tutorials', methods=['POST', 'GET'])
def receive_tutorial():
    db = retrieve_db('Tutorial', 'video')
    tutorial = list(db.values())
    tutorial_list = []
    for video in tutorial:
        tutorial_list.append(video)
    return render_template('tutorial.html', tutorial_list=tutorial_list)


if __name__ == '__main__':
    app.run(debug=True)
