class Address:
    count_id = 0

    # initializer method
    def __init__(self, first_name, last_name, town, zipcode, address, phone_number, office_number, email_address, remarks):
        Address.count_id += 1
        self.__user_id = Address.count_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__town = town
        self.__zipcode = zipcode
        self.__address = address
        self.__phone_number = phone_number
        self.__office_number = office_number
        self.__email_address = email_address
        self.__remarks = remarks

    # accessor methods
    def get_user_id(self):
        return self.__user_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_town(self):
        return self.__town

    def get_zipcode(self):
        return self.__zipcode

    def get_address(self):
        return self.__address

    def get_phone_number(self):
        return self.__phone_number

    def get_office_number(self):
        return self.__office_number

    def get_email_address(self):
        return self.__email_address

    def get_remarks(self):
        return self.__remarks

    # mutator methods
    def set_user_id(self, user_id):
        self.__user_id = user_id

    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_town(self, town):
        self.__town = town

    def set_zipcode(self, zipcode):
        self.__zipcode = zipcode

    def set_address(self, address):
        self.__address = address

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_office_number(self, office_number):
        self.__office_number = office_number

    def set_email_address(self, email_address):
        self.__email_address = email_address

    def set_remarks(self, remarks):
        self.__remarks = remarks
