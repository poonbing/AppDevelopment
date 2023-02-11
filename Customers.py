class Customers:


    def __init__(self, customer_id, first_name, last_name, email, username, password, contact, gender, dob):
        self.__customer_id = customer_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__username = username
        self.__password = password
        self.__contact = contact
        self.__gender = gender
        self.__dob = dob
        self.__points = "0"
        self.__rank = "Bronze"
        self.__status = "Active"

    #SETTER
    def set_customer_id(self,customer_id):
        self.__customer_id = customer_id
    def set_first_name(self,first_name):
        self.__first_name = first_name
    def set_last_name(self,last_name):
        self.__last_name = last_name
    def set_email(self,email):
        self.__email = email
    def set_username(self,username):
        self.__username = username
    def set_password(self,password):
        self.__password = password
    def set_contact(self,contact):
        self.__contact = contact
    def set_gender(self,gender):
        self.__gender = gender
    def set_dob(self,dob):
        self.__dob = dob
    def set_points(self,points):
        self.__points = "0"
    def set_rank(self,rank):
        self.__rank = 'Bronze'
    def set_status(self,status):
        if status == "Locked":
            self.__status = 'Locked'
        else:
            self.__status = 'Active'


    #GETTER
    def get_customer_id(self):
        return self.__customer_id
    def get_first_name(self):
        return self.__first_name
    def get_last_name(self):
        return self.__last_name
    def get_email(self):
        return self.__email
    def get_username(self):
        return self.__username
    def get_password(self):
        return self.__password
    def get_contact(self):
        return self.__contact
    def get_gender(self):
        return self.__gender
    def get_dob(self):
        return self.__dob
    def get_points(self):
        return self.__points
    def get_rank(self):
        return self.__rank
    def get_status(self):
        return self.__status
