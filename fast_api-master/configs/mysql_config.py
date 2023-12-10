import mysql.connector

dbconfig = {
    "host": "localhost",
    "port": "3306",
    "username": "phpmyadmin",
    "password": "123456789",
    "database": "futurelove"
}


class My_Connection:
    def __init__(self):
        self.con = None
        self.cur = None

    def __enter__(self):
        self.con = mysql.connector.connect(host=dbconfig['host'], user=dbconfig['username'],
                                           password=dbconfig['password'], database=dbconfig['database'])
        self.con.autocommit = True
        self.cur = self.con.cursor(dictionary=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.con is not None:
            self.con.close()
