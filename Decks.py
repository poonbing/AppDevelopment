class Deck:
    def __init__(self, id_count, name, brand, deck_type, description, price, image, offer):
        self.offered_price = None
        self.product_id = id_count + 1
        self.name = name
        self.brand = brand
        self.type = deck_type
        self.description = description
        self.price = f"{float(price):.2f}"
        self.image = image
        self.offer = offer

    def set_product_id(self, product_id):
        self.product_id = product_id

    def get_product_id(self):
        return self.product_id

    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def set_brand(self, brand):
        self.brand = brand

    def get_brand(self):
        return self.brand

    def set_type(self, deck_type):
        self.type = deck_type

    def get_type(self):
        return self.type

    def set_description(self, description):
        self.description = description

    def get_description(self):
        return self.description

    def set_price(self, price):
        self.price = price

    def get_price(self):
        return self.price

    def set_image(self, image):
        self.image = image

    def get_image(self):
        return self.image

    def set_offer(self, offer):
        self.offer = offer

    def get_offer(self):
        return self.offer

    def get_offered_price(self):
        of = float(float(self.price)*((100 - int(self.offer)) / 100))
        self.offered_price = f"{of:.2f}"
        return self.offered_price

