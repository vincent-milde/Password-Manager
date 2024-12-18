import sqlite3

'''
Create a Database that stores a domain with a username and password bound to it

create methods to: 
    add/delete passwords
    fetch/edit Data
    search data by domain
'''


class PasswordDataBase ():
    def __init__(self):
        super.__init__(self)
        #connecting/creating the database
        self.connection = sqlite3.connect("passwords.db")

        #Cursor for commands and stuff
        self.cursor = self.connection.cursor()

        #Main Table/format for storing the data
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL
            username TEXT NOT NULL,
            password TEXT NOT NULL
            )               
            """)

    def get_domains(self):
        pass
        #return domains
    def add_password(self):
        pass
    def delete_password(self):
        pass
    def fetch_data(self):
        pass
    def edit_data(self):
        pass
    def search_by_domain(self,domain):
        pass