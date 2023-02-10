from flask import Flask, render_template, request, url_for, redirect, session
import shelve
from Form1 import CreateDeckForm, UpdateDeckForm, CreateTutorial, CreateAccessories, UpdateTutorial, UpdateAccessories
from Decks import Deck
import random
from werkzeug.utils import secure_filename
import os


app = Flask('__name__', template_folder='./templates/')
app.config['SECRET_KEY'] = 'SecretKey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'


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


def unify_id(shelve_name, key):
    db = retrieve_db(shelve_name, key)
    keys = db.keys()
    for key in keys:
        item = db[key]
        item['id'] = key
        db[key] = item
    commit_db('products', 'decks', db)


print(retrieve_db('user', 'session'))


# --Lewis--:Homepage
@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        product_id = request.form.get("id")
        print(product_id)
        session['id'] = product_id
        return redirect(url_for('product_page'))
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
        amount = session['cart']
        return render_template('home.html', top_items=topitems, new_items=newitems, amount=amount)


@app.route('/decks_database', methods=['GET', 'POST', 'PUT'])
def decks_database():
    form = CreateDeckForm()
    if request.method == "GET":
        product = retrieve_db('products', 'decks')
        product_list = product.values()
        amount = session['cart']
        return render_template('decks-database.html', form=form, product_list=product_list, product=product, amount=amount)
    elif request.method == 'POST':
        if request.form.get('submit') == 'create':
            file = form.file.data
            if form.file.data is not None:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                uid = unique_id('decks')
                product = {
                    'id': uid,
                    'name': form.name.data,
                    'brand': form.brand.data,
                    'type': form.type.data,
                    'description': form.description.data,
                    'price': f"{form.price.data:.2f}",
                    'image': filename,
                    'offer': form.offer.data,
                    'offered price': offered_price(form.price.data, form.offer.data)
                }
                db = retrieve_db('products', 'decks')
                db[uid] = product
                commit_db('products', 'decks', db)
                print('created')
                return redirect(url_for('decks_database'))
            else:
                return redirect(url_for('decks_database'))
        elif request.form.get('function') == 'delete':
            delete_id = request.form.get('submit')
            print(delete_id)
            db = retrieve_db('products', 'decks')
            db.pop(delete_id)
            print(db)
            commit_db('products', 'decks', db)
            return redirect(url_for('decks_database'))
        elif request.form.get('function') == 'update':
            db = retrieve_db('products', 'decks')
            pid = request.form.get('submit')
            item = db[pid]
            form = UpdateDeckForm()
            amount = session['cart']
            return render_template('decks-update.html', id=pid, item=item, form=form, amount=amount)
        else:
            form = UpdateDeckForm()
            db = retrieve_db('products', 'decks')
            uid = request.form.get('submit')
            print(uid)
            product = db[uid]
            if form.file.data is not None:
                file = form.file.data
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                product['image'] = filename
            if form.name.data != "":
                product['name'] = form.name.data
                print('name')
            if form.brand.data != "":
                product['brand'] = form.brand.data
            if form.type.data is not None:
                product['type'] = form.type.data
                print('type')
            if form.description.data != "":
                product['description'] = form.description.data
                print('description')
            if form.price.data is not None:
                product['price'] = f"{form.price.data:.2f}"
                print('price')
            if form.offer.data is not None:
                print('offer change')
                product['offer'] = form.offer.data
                product['offered price'] = offered_price(product['price'], product['offer'])
            db[uid] = product
            commit_db('products', 'decks', db)
            print("updated")
            return redirect(url_for('decks_database'))


@app.route('/retrieveluxuryDecks', methods=['GET', 'POST'])
def retrieve_luxury():
    if request.method == 'POST':
        product_list = retrieve_db('products', 'decks')
        product_id = request.form.get("id")
        print(product_id)
        product = [product_list[product_id]]
        print(product)
        amount = session['cart']
        return render_template("product-index.html", products=product, amount=amount)
    else:
        db = retrieve_db('products', 'decks')
        data = list(db.values())
        products = []
        for product in data:
            if product['type'] == "Luxury":
                products.append(product)
            else:
                pass
        amount = session['cart']
        return render_template('retrieveluxuryDecks.html', products=products, amount=amount)


@app.route('/retrieveclassicDecks', methods=['GET', 'POST'])
def retrieve_classic():
    if request.method == 'POST':
        product_list = retrieve_db('products', 'decks')
        product_id = request.form.get("id")
        print(product_id)
        product = [product_list[product_id]]
        print(product)
        amount = session['cart']
        return render_template("product-index.html", products=product, amount=amount)
    else:
        db = retrieve_db('products', 'decks')
        data = list(db.values())
        products = []
        for product in data:
            if product['type'] == "Classic":
                products.append(product)
            else:
                pass
        amount = session['cart']
        return render_template('retrieveclassicDecks.html', products=products, amount=amount)


@app.route('/retrievecardistryDecks', methods=['GET', 'POST'])
def retrieve_cardistry():
    if request.method == 'POST':
        product_list = retrieve_db('products', 'decks')
        product_id = request.form.get("id")
        print(product_id)
        product = [product_list[product_id]]
        print(product)
        amount = session['cart']
        return render_template("product-index.html", products=product, amount=amount)
    else:
        db = retrieve_db('products', 'decks')
        data = list(db.values())
        products = []
        for product in data:
            if product['type'] == "Cardistry":
                products.append(product)
            else:
                pass
        amount = session['cart']
        return render_template('retrievecardistryDecks.html', products=products, amount=amount)
# --Lewis--:Homepage end


# --BP--:Product view start
@app.route('/product_page', methods=['POST', 'GET'])
def product_page():
    if request.method == 'GET':
        product_id = session['id']
        product_list = retrieve_db('products', 'decks')
        access_list = retrieve_db('products', 'accessories')
        if product_id in product_list:
            products = product_list[product_id]
            amount = session['cart']
            return render_template("product-index.html", products=products, amount=amount)
        elif product_id in access_list:
            products = access_list[product_id]
            amount = session['cart']
            return render_template("product-index.html", products=products, amount=amount)
    elif request.method == "POST":
        select_id = request.form.get('submit')
        print(select_id)
        quantity = request.form.get('quantity')
        db = retrieve_db('user', 'session')
        x = db.keys()
        for i in x:
            key = i
        cart = db[key]['cart']
        if select_id in cart.keys():
            item = cart[select_id]
            existing = item['quantity']
            quantity = int(int(existing)+int(quantity))
            item['quantity'] = quantity
            price = item['price']
            total = f'{float(float(price)*int(quantity)):.2f}'
            item['total'] = total
            cart[select_id] = item
            commit_db('user', 'session', db)
        elif select_id not in cart.keys():
            price = request.form.get('price')
            total = f'{float(float(price)*int(quantity)):.2f}'
            item = {
                'id': select_id,
                'quantity': quantity,
                'price': price,
                'total': total,
                'brand': request.form.get('brand')
            }
            db[key]['cart'][select_id] = item
            commit_db('user', 'session', db)
        product_list = retrieve_db('products', 'decks')
        access_list = retrieve_db('products', 'accessories')
        if select_id in product_list:
            products = product_list[select_id]
        elif select_id in access_list:
            products = access_list[select_id]
        amount = len(cart.keys())
        session['cart'] = amount
        amount = session['cart']
        return render_template("product-index.html", products=products, amount=amount)
# --BP--:Product view end


@app.route('/accessories_database', methods=['POST', 'GET'])
def accessories_database():
    form = CreateAccessories()
    if request.method == 'GET':
        form = UpdateAccessories()
        product = retrieve_db('products', 'accessories')
        product_list = product.values()
        amount = session['cart']
        return render_template('accessories-database.html', form=form, product_list=product_list, product=product, amount=amount)
    elif request.method == 'POST':
        if request.form.get('submit') == 'create':
            print('creating')
            file = form.file.data
            if form.file.data is not None:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                uid = unique_id('accessories')
                product = {
                    'id': uid,
                    'name': form.name.data,
                    'brand': form.brand.data,
                    'description': form.description.data,
                    'price': f"{form.price.data:.2f}",
                    'image': filename,
                    'offer': form.offer.data,
                    'offered price': offered_price(form.price.data, form.offer.data)
                }
                db = retrieve_db('products', 'accessories')
                db[uid] = product
                commit_db('products', 'accessories', db)
                print('created')
                return redirect(url_for('accessories_database'))
        elif request.form.get('function') == 'delete':
            delete_id = request.form.get('submit')
            print(delete_id)
            db = retrieve_db('products', 'accessories')
            db.pop(delete_id)
            commit_db('products', 'accessories', db)
            print("deleted")
            return redirect(url_for('accessories_database'))
        elif request.form.get('function') == 'update':
            db = retrieve_db('products', 'accessories')
            pid = request.form.get('submit')
            item = db[pid]
            form = UpdateDeckForm()
            amount = session['cart']
            return render_template('accessories-update.html', item=item, form=form, amount=amount)
        else:
            db = retrieve_db('products', 'accessories')
            uid = request.form.get('submit')
            print(uid)
            product = db[uid]
            if form.file.data is not None:
                file = form.file.data
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                product['image'] = filename
            if form.name.data != "":
                product['name'] = form.name.data
                print('name')
            if form.brand.data != "":
                product['brand'] = form.brand.data
            if form.description.data != "":
                product['description'] = form.description.data
            if form.price.data is not None:
                product['price'] = f"{form.price.data:.2f}"
            if form.offer.data is not None:
                print('offer change')
                product['offer'] = form.offer.data
                product['offered price'] = offered_price(product['price'], product['offer'])
            uid = str(uid)
            db[uid] = product
            commit_db('products', 'accessories', db)
            print("updated")
            return redirect(url_for('accessories_database'))


@app.route('/accessories_database/update', methods=['POST', 'GET'])
def update_accessories_info():
    form = UpdateDeckForm()
    if request.method == "POST":
        db = retrieve_db('products', 'decks')
        uid = request.form.get('product_id')
        print(uid)
        product = db[uid]
        if form.file.data is not None:
            file = form.file.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            product['image'] = filename
        if form.name.data != "":
            product['name'] = form.name.data
            print('name')
        if form.brand.data != "":
            product['brand'] = form.brand.data
        if form.description.data != "":
            product['description'] = form.description.data
        if form.price.data is not None:
            product['price'] = f"{form.price.data:.2f}"
        if form.offer.data is not None:
            print('offer change')
            product['offer'] = form.offer.data
            product['offered price'] = offered_price(product['price'], product['offer'])
        uid = str(uid)
        db[uid] = product
        commit_db('products', 'decks', db)
        print("updated")
        return redirect(url_for('accessories_database'))
    else:
        amount = session['cart']
        return render_template("accessories-update.html", form=form, amount=amount)


@app.route('/accessories', methods=['GET', 'POST'])
def retrieve_accessories():
    if request.method == 'POST':
        product_id = request.form.get("id")
        print(product_id)
        session['id'] = product_id
        return redirect(url_for('product_page'))
    else:
        db = retrieve_db('products', 'accessories')
        data = list(db.values())
        products = []
        for product in data:
            products.append(product)
        amount = session['cart']
        return render_template('accessories.html', products=products, amount=amount)


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
        amount = session['cart']
        return render_template('createTutorial.html', form=form, tutorial_list=tutorial_list, video=video, amount=amount)


@app.route('/tutorials', methods=['POST', 'GET'])
def receive_tutorial():
    db = retrieve_db('Tutorial', 'video')
    tutorial = list(db.values())
    tutorial_list = []
    for video in tutorial:
        tutorial_list.append(video)
    amount = session['cart']
    return render_template('tutorial.html', tutorial_list=tutorial_list, amount=amount)


if __name__ == '__main__':
    app.run(debug=True)
