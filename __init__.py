from flask import Flask, render_template, request, url_for, redirect, session, g
import shelve
from Forms import signUp, Login, update, ForgetPassword
from Form1 import CreateDeckForm, UpdateDeckForm, CreateTutorial, CreateAccessories, UpdateTutorial, UpdateAccessories
from uuid import uuid4
import random
from werkzeug.utils import secure_filename
import os
import os.path
from flask_mail import Mail,Message
import Customers

app = Flask('__name__', template_folder='./templates/')
app.config['SECRET_KEY'] = 'SecretKey'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'appdevresetpw@gmail.com'
app.config['MAIL_PASSWORD'] = 'ydhqmpownjvqdnxl'
mail = Mail(app)


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
    with shelve.open(shelve_name) as db:
        output = db[key]
    count = 1
    for keys in output:
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
    elif type == 'tutorial':
        kind = 'T'
        db = retrieve_db('Tutorial', 'video')
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


@app.before_request
def get_current_user():
    customers_dict = {}
    db = shelve.open('customers.db', 'r')
    try:
        customers_dict = db['Customers']
    except:
        print("error bitch")

    try:
        g.current_user = customers_dict[session['current_user']]
    except KeyError:
        g.current_user = None


# --Lewis--:Homepage
@app.route("/", methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        product_id = request.form.get("id")
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
        all_product_list = []
        accessories_db = retrieve_db('products', 'accessories')
        accessories_info = list(accessories_db.values())
        product_info = list(db.values())
        for items in accessories_info:
            all_product_list.append(items)
        for deck in product_info:
            all_product_list.append(deck)
        product_amount = len(all_product_list)
        products = random.sample(all_product_list, product_amount)
        shopping = retrieve_db('user', 'session')
        x = shopping.keys()
        for i in x:
            cart = shopping[i]['cart']
        count = 0
        if len(cart) != 0:
            for item in cart:
                count += 1
        session['cart'] = count
        amount = session['cart']
        return render_template('home.html', top_items=topitems, new_items=newitems, amount=amount, products=products)


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
                return redirect(url_for('decks_database'))
            else:
                return redirect(url_for('decks_database'))
        elif request.form.get('function') == 'delete':
            delete_id = request.form.get('submit')
            db = retrieve_db('products', 'decks')
            db.pop(delete_id)
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
            product = db[uid]
            if form.file.data is not None:
                file = form.file.data
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                product['image'] = filename
            if form.name.data != "":
                product['name'] = form.name.data
            if form.brand.data != "":
                product['brand'] = form.brand.data
            if form.type.data is not None:
                product['type'] = form.type.data
            if form.description.data != "":
                product['description'] = form.description.data
            if form.price.data is not None:
                product['price'] = f"{form.price.data:.2f}"
            if form.offer.data is not None:
                product['offer'] = form.offer.data
                product['offered price'] = offered_price(product['price'], product['offer'])
            db[uid] = product
            commit_db('products', 'decks', db)
            return redirect(url_for('decks_database'))


@app.route('/retrieveallDecks', methods=['GET', 'POST'])
def retrieve_classic():
    if request.method == 'POST':
        product_list = retrieve_db('products', 'decks')
        product_id = session['id']
        product = product_list[product_id]
        amount = session['cart']
        return render_template("product-index.html", products=product, amount=amount)
    else:
        db = retrieve_db('products', 'decks')
        data = list(db.values())
        products = []
        for product in data:
            products.append(product)
        amount = session['cart']
        return render_template('retrieveallDecks.html', products=products, amount=amount)
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
            relate = []
            related = []
            prod = product_list
            for key in prod.keys():
                relate.append(key)
            relate.remove(product_id)
            related_list = random.sample(relate, k=4)
            for key in related_list:
                related.append(prod[key])
            print(related)
            amount = session['cart']
            return render_template("product-index.html", products=products, amount=amount, related=related)
        elif product_id in access_list:
            products = access_list[product_id]
            relate = []
            related = []
            access = access_list
            for key in access.keys():
                relate.append(key)
            relate.pop(product_id)
            related_list = random.sample(relate, k=4)
            for key in related_list:
                related.append(access[key])
            amount = session['cart']
            return render_template("product-index.html", products=products, amount=amount, related=related)
    elif request.method == "POST":
        select_id = request.form.get('submit')
        quantity = request.form.get('quantity')
        db = retrieve_db('user', 'session')
        x = db.keys()
        for i in x:
            key = i
        session['cart key'] = key
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
        amount = len(cart.keys())
        session['cart'] = amount
        return redirect(url_for('product_page'))
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
                return redirect(url_for('accessories_database'))
        elif request.form.get('function') == 'delete':
            delete_id = request.form.get('submit')
            db = retrieve_db('products', 'accessories')
            db.pop(delete_id)
            commit_db('products', 'accessories', db)
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
            product = db[uid]
            if form.file.data is not None:
                file = form.file.data
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                product['image'] = filename
            if form.name.data != "":
                product['name'] = form.name.data
            if form.brand.data != "":
                product['brand'] = form.brand.data
            if form.description.data != "":
                product['description'] = form.description.data
            if form.price.data is not None:
                product['price'] = f"{form.price.data:.2f}"
            if form.offer.data is not None:
                product['offer'] = form.offer.data
                product['offered price'] = offered_price(product['price'], product['offer'])
            uid = str(uid)
            db[uid] = product
            commit_db('products', 'accessories', db)
            return redirect(url_for('accessories_database'))


@app.route('/accessories_database/update', methods=['POST', 'GET'])
def update_accessories_info():
    form = UpdateDeckForm()
    if request.method == "POST":
        db = retrieve_db('products', 'decks')
        uid = request.form.get('product_id')
        product = db[uid]
        if form.file.data is not None:
            file = form.file.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            product['image'] = filename
        if form.name.data != "":
            product['name'] = form.name.data
        if form.brand.data != "":
            product['brand'] = form.brand.data
        if form.description.data != "":
            product['description'] = form.description.data
        if form.price.data is not None:
            product['price'] = f"{form.price.data:.2f}"
        if form.offer.data is not None:
            product['offer'] = form.offer.data
            product['offered price'] = offered_price(product['price'], product['offer'])
        uid = str(uid)
        db[uid] = product
        commit_db('products', 'decks', db)
        return redirect(url_for('accessories_database'))
    else:
        amount = session['cart']
        return render_template("accessories-update.html", form=form, amount=amount)


@app.route('/accessories', methods=['GET', 'POST'])
def retrieve_accessories():
    if request.method == 'POST':
        product_id = request.form.get("id")
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
    form = CreateTutorial()
    if request.method == 'POST':
        if request.form.get('submit') == 'create':
            file = form.file.data
            if form.file.data is not None:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
                uid = unique_id('tutorial')
                video = {
                    'id': uid,
                    'name': form.name.data,
                    'difficulty': form.difficulty.data,
                    'type': form.type.data,
                    'video': form.video.data,
                    'thumbnail': filename,
                }
                db = retrieve_db('Tutorial', 'video')
                db[uid] = video
                commit_db('Tutorial', 'video', db)
                return redirect(url_for('create_tutorial'))
        elif request.form.get('function') == 'delete':
            if request.form.get('function') == "delete":
                delete_id = request.form.get('submit')
                product = retrieve_db('Tutorial', 'video')
                cid = str(delete_id)
                product.pop(cid)
                commit_db('Tutorial', 'video', product)
                return redirect(url_for('create_tutorial'))
        elif request.form.get('function') == 'update':
            db = retrieve_db('Tutorial', 'video')
            pid = request.form.get('submit')
            item = db[pid]
            form = UpdateTutorial()
            amount = session['cart']
            return render_template('tutorial-update.html', video=item, form=form, amount=amount)
    else:
        video = retrieve_db('Tutorial', 'video')
        tutorial_list = video.values()
        amount = session['cart']
        return render_template('createTutorial.html', form=form, tutorial_list=tutorial_list, video=video, amount=amount)


@app.route('/tutorial_update', methods=['POST', 'GET'])
def update_tutorial_info():
    form = UpdateTutorial()
    if request.method == "POST":
        db = retrieve_db('Tutorial', 'video')
        uid = request.form.get('product_id')
        product = db[uid]
        if form.file.data is not None:
            file = form.file.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
            product['image'] = filename
        if form.name.data != "":
            product['name'] = form.name.data
        elif form.difficulty.data is not None:
            product['difficulty'] = form.difficulty.data
        elif form.type.data is not None:
            product['type'] = form.type.data
        elif form.video.data is not None:
            product['video'] = form.video.data
        uid = str(uid)
        db[uid] = product
        commit_db('Tutorial', 'video', db)
        return redirect(url_for('create_tutorial'))
    else:
        return render_template('tutorial-update.html', form=form)


@app.route('/tutorials', methods=['POST', 'GET'])
def receive_tutorial():
    db = retrieve_db('Tutorial', 'video')
    tutorial = list(db.values())
    tutorial_list = []
    for video in tutorial:
        tutorial_list.append(video)
    amount = session['cart']
    return render_template('tutorial.html', tutorial_list=tutorial_list, amount=amount)


@app.route('/Promotion', methods=['POST', 'GET'])
def retrieve_promotion():
    promotion_list = []
    product_db = retrieve_db('products', 'decks')
    product_info = list(product_db.values())
    for deck in product_info:
        if deck['offered price'] != deck['price']:
            promotion_list.append(deck)
        else:
            pass
    accessories_db = retrieve_db('products', 'accessories')
    accessories_info = list(accessories_db.values())
    for items in accessories_info:
        if items['offered price'] != items['price']:
            promotion_list.append(items)
        else:
            pass
    if request.method == 'POST':
        product_id = request.form.get("id")
        session['id'] = product_id
        return redirect(url_for('product_page'))
    return render_template('retrievePromotion.html', promotion_list=promotion_list)


@app.route('/cart', methods=['POST', 'GET'])
def retrieve_cart():
    if request.method == 'GET':
        db = retrieve_db('user', 'session')
        decks = retrieve_db('products', 'decks')
        access = retrieve_db('products', 'accessories')
        x = db.keys()
        for i in x:
            cart = db[i]['cart']
        keys = cart.keys()
        cart_list = []
        for key in keys:
            item = {}
            if key[0] == 'D':
                deck = decks[key]
                item['id'] = key
                item['name'] = deck['name']
                item['type'] = 'Decks'
                item['quantity'] = cart[key]['quantity']
                item['price'] = deck['offered price']
                item['total'] = f"{float(deck['offered price'])*float(cart[key]['quantity']):.2f}"
                item['image'] = deck['image']
                cart_list.append(item)
            elif key[0] == 'A':
                acc = access[key]
                item['id'] = key
                item['name'] = acc['name']
                item['type'] = 'Accessories'
                item['quantity'] = cart[key]['quantity']
                item['price'] = acc['offered price']
                item['total'] = f"{float(acc['offered price'])*float(cart[key]['quantity']):.2f}"
                item['image'] = acc['image']
                cart_list.append(item)
        count = 0
        price = 0
        for i in cart_list:
            count += int(i['quantity'])
            price += float(i['total'])
        price = f"{price:.2f}"
        amount = session['cart']
        return render_template('shopping-cart.html', cart_list=cart_list, amount=amount, count=count, total=price)


@app.route('/deletecartitem/<id>', methods=['GET'])
def deletecartitem(id):
    db = retrieve_db('user', 'session')
    x = db.keys()
    for i in x:
        cart = db[i]['cart']
    shop = cart
    keys = shop.keys()
    for key in keys:
        try:
            cart.pop(id)
            break
        except:
            pass
    for i in x:
        db[i]['cart'] = cart
    commit_db('user', 'session', db)
    count = 0
    for i in cart:
        count += 1
    session['cart'] = count
    return redirect(url_for('retrieve_cart'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = Login(request.form)
    if request.method == 'POST' and login_form.validate():
        emails = []
        customers_dict = {}
        db = shelve.open('customers.db', 'c')
        session_dict = shelve.open('session.db', 'c')
        user_id_dict = {}
        try:
            if 'current_session' in session_dict:
                user_id_dict = session_dict['current_session']
            else:
                session_dict['current_session'] = user_id_dict
        except:
            print("error")

        try:
            customers_dict = db['Customers']
        except:
            print("error in retrieving db")

        for key in customers_dict:
            customer = customers_dict.get(key)
            email = customer.get_email()
            password = customer.get_password()
            userid = customer.get_customer_id()

            if login_form.email.data == email:
                if login_form.password.data == password:
                    if email.split('@')[1] == "cardhouse.com":
                        session['current_user'] = customer.get_customer_id()
                        return redirect(url_for('AdminDashboard'))
                    else:
                        user_id_dict['user_id'] = userid
                        session_dict['current_session'] = user_id_dict
                        customers_dict[customer.get_customer_id()] = customer
                        db['Customers'] = customers_dict
                        session['login_success'] = customer.get_email()
                        db.close()
                        return redirect(url_for('profile'))

                else:
                    session['wrong_password'] = "WRONG PASSWORD"
            else:
                print("email dont exist")
        session['email_dont_exist'] = "EMAIL DOES NOT EXIST"

    return render_template('/UserInt_Login.html', form=login_form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    signup_form = signUp(request.form)
    if request.method == 'POST' and signup_form.validate():
        emails = []
        customers_dict = {}
        db = shelve.open('customers.db', 'c')

        try:
            customers_dict = db['Customers']
        except:
            print("error in retrieving db")

        for key in customers_dict:
            customer = customers_dict.get(key)
            emails.append(customer.get_email())

        temp_id = str(random.randint(100, 999))


        if signup_form.email.data.split('@')[1] == "cardhouse.com":
            session['banned_email'] = "Emails cannot end with '@cardhouse.com'"
            return redirect(url_for('signup'))

        elif signup_form.email.data in emails:
            session['email_exist'] = 'already exists'
            return redirect(url_for('signup'))
        else:
            customer = Customers.Customers("U"+temp_id,
                                          signup_form.first_name.data,
                                          signup_form.last_name.data,
                                          signup_form.email.data,
                                          signup_form.username.data,
                                          signup_form.password.data,
                                          signup_form.contact.data,
                                          signup_form.gender.data,
                                          signup_form.dob.data)

        customers_dict[customer.get_customer_id()]=customer
        db['Customers'] = customers_dict
        print(customer.get_first_name(), customer.get_last_name(), "was stored in db successfully with user_id ==",
        customer.get_customer_id())
        db.close()

        session['account_created'] = signup_form.email.data

    return render_template('/UserInt_signup.html', form=signup_form)


@app.route('/profile')
def profile():
    customers_dict = {}
    customer = ""
    db = shelve.open('customers.db', 'r')
    customers_dict = db['Customers']
    for key in customers_dict:
        print(session['login_success'], customers_dict.get(key).get_email())
        if session['login_success'] == customers_dict.get(key).get_email():
            customer = customers_dict.get(key)
    return render_template('/UserInt_profile.html', customer=customer)


@app.route('/customers')
def customers():
    form = update(request.form)
    db = shelve.open('customers.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        if customer.get_email().split('@')[1] != "cardhouse.com":
            customers_list.append(customer)

    return render_template("/UserInt_customers.html", count=len(customers_list), customers_list=customers_list, form=form, customer=customer)

@app.route('/admins')
def admins():

    db = shelve.open('customers.db', 'r')
    customers_dict = db['Customers']
    db.close()

    customers_list = []
    for key in customers_dict:
        customer = customers_dict.get(key)
        if customer.get_email().split('@')[1] == "cardhouse.com":
            customers_list.append(customer)

    return render_template("/UserInt_admin.html", count=len(customers_list), customers_list=customers_list)


@app.route('/updateCustomer/<id>/', methods=['POST'])
def update_user(id):
    form = update(request.form)
    if request.method == 'POST' and form.validate():
        emails = []
        customers_dict = {}
        db = shelve.open('customers.db', 'w')
        customers_dict = db['Customers']

        customer = customers_dict.get(id)
        customer.set_first_name(form.first_name.data)
        customer.set_last_name(form.last_name.data)
        customer.set_username(form.username.data)
        customer.set_contact(form.contact.data)
        customer.set_gender(form.gender.data)
        customer.set_dob(form.dob.data)


        db['Customers'] = customers_dict
        db.close()

        return redirect(url_for('customers'))



@app.route('/deleteCustomer/<id>', methods=['POST'])
def delete_customer(id):
    customers_dict = {}
    db = shelve.open('customers.db', 'w')
    customers_dict = db['Customers']
    customers_dict.pop(id)
    db['Customers'] = customers_dict
    db.close()
    return redirect(url_for('customers'))


@app.route('/Cart', methods=['GET', 'POST'])
def Shopcart():
    return render_template('/UserInt_Cart.html')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('login_success', None)
    return redirect(url_for('login'))


@app.route('/AdminDash', methods=['GET', 'POST'])
def AdminDashboard():
    return render_template('/UserInt_AdminDash.html')

# @app.route('/ForgetPassword', methods=['GET', 'POST'])
# def ForgetPassword():
    # forget_password_form = ForgetPassword(request.form)
    # if request.method == 'POST' and forget_password_form.validate():
    #     accounts = []
    #     accounts_dict = {}
    #     db = shelve.open('customers.db', 'c')
    #     try
    #         accounts_dict = db['Customers']
    #     except:
    #         print("error")
    #
    #     for key in accounts_dict:
    #         customer = accounts_dict.get(key)
    #         accounts.append(customer)
    #
    #     for customer in accounts:
    #         if forget_password_form.email.data == customer.get_email():
    #             temporary_password = str(uuid4())[:8]
    #             customer.set_password(temporary_password)
    #             accounts_dict[customer.get_customer_id()] = customer
    #             db['Customers'] = accounts_dict
    #             db.close()
    #             msg = Message('Your new password', sender='appdevprojectsss@gmail.com', recipients=[forget_password_form.email.data])
    #             msg.html = render_template('email.html', temporary_password=temporary_password)
    #             mail.send(msg)
    #             session['email_sent'] = forget_password_form.email.data
    #             return redirect(url_for('login'))
    #         session['emailnotfound'] = "EMail not found"
    #         return redirect(url_for('password'))
    # else:
    #     print("error")

    # return render_template('/UserInt_forgotpass.html', form=forget_password_form)


@app.route('/AdminDashChart', methods=['GET', 'POST'])
def AdminDashboardChart():
    return render_template('/Dashboard/UserInt_AdminDash_charts.html')

@app.route('/Forgotpass', methods=['GET', 'POST'])
def Forgotpassword():
    forget_password_form = ForgetPassword(request.form)
    if request.method == 'POST' and forget_password_form.validate():
        accounts = []
        accounts_dict = {}
        db = shelve.open('customers.db', 'c')
        try:
            accounts_dict = db['Customers']
        except:
            print("error opening db")

        for key in accounts_dict:
            customer = accounts_dict.get(key)
            accounts.append(customer)

        for customer in accounts:
            print("Hello", customer.get_email())
            if forget_password_form.email.data == customer.get_email():
                temporary_password = str(uuid4())[:8]
                customer.set_password(temporary_password)
                accounts_dict[customer.get_customer_id()] = customer
                db['Customers'] = accounts_dict
                db.close()
                msg = Message('Your new password', sender='appdevprojectsss@gmail.com', recipients=[forget_password_form.email.data])
                msg.html = render_template('email.html', temporary_password=temporary_password)
                mail.send(msg)
                session['email_sent'] = forget_password_form.email.data
                return redirect(url_for('login'))
        session['emailnotfound'] = "Email not found"
        return redirect(url_for('Forgotpassword'))
    else:
        print("not validating")

    return render_template('/UserInt_forgot.html', form=forget_password_form)

# @app.route('/AdminDashTable', methods=['GET', 'POST'])
# def AdminDashboardTable():
#     return render_template('/Dashboard/UserInt_customers.html')


if __name__ == '__main__':
    app.run(debug=True)
