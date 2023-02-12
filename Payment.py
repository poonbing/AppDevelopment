class Payment:
    count_id = 0

    # initializer method
    def __init__(self, card_name, card_number, security_code, expiry_month, expiry_year, payment_type, delivery_type, promo_code):
        Payment.count_id += 1
        self.__user_id = Payment.count_id
        self.__card_name = card_name
        self.__card_number = card_number
        self.__security_code = security_code
        self.__expiry_month = expiry_month
        self.__expiry_year = expiry_year
        self.__payment_type = payment_type
        self.__delivery_type = delivery_type
        self.__promo_code = promo_code

    # accessor methods
    def get_user_id(self):
        return self.__user_id

    def get_card_name(self):
        return self.__card_name

    def get_card_number(self):
        return self.__card_number

    def get_security_code(self):
        return self.__security_code

    def get_expiry_month(self):
        return self.__expiry_month

    def get_expiry_year(self):
        return self.__expiry_year

    def get_payment_type(self):
        return self.__payment_type

    def get_delivery_type(self):
        return self.__delivery_type

    def get_promo_code(self):
        return self.__promo_code

    # mutator methods
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_card_name(self, card_name):
        self.__card_name = card_name

    def set_card_number(self, card_number):
        self.__card_number = card_number

    def set_security_code(self, security_code):
        self.__security_code = security_code

    def set_expiry_month(self, expiry_month):
        self.__expiry_month = expiry_month

    def set_expiry_year(self, expiry_year):
        self.__expiry_year = expiry_year

    def set_payment_type(self, payment_type):
        self.__payment_type = payment_type

    def set_delivery_type(self, delivery_type):
        self.__delivery_type = delivery_type

    def set_promo_code(self, promo_code):
        self.__promo_code = promo_code
