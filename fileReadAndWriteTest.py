import sqlite3
import sqlcipher
'''
Create a Database that stores a domain with a username and password bound to it

create methods to: 
    add/delete passwords
    fetch/edit Data
    search data by domain
'''


class PasswordDataBase ():
    def __init__(self):
        #connect to the database
        self.connect()
        #Main Table/format for storing the data
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL,
            password TEXT NOT NULL
            )               
            """)
    def connect(self):
        #connect to the database
        self.connection = sqlite3.connect("passwords.db")
        self.cursor = self.connection.cursor()
        
    def get_domains(self):
        #connect to the database
        self.connect()
        
        #select all domains from the database
        self.cursor.execute("SELECT domain FROM passwords")
        #fetch all domains
        domains = self.cursor.fetchall()
        #return the domains
        return domains
    
    def add_entry(self, domain, username, password):
        #connect to the database
        self.connect()
        
        #add a domain, username and password at the same time
        self.cursor.execute("INSERT INTO passwords (domain, username, password) VALUES (?,?,?)", (domain, username, password))
        self.connection.commit()
        self.connection.close()    

    def delete_entry(self, domain):
        #connect to the database
        self.connect()  
        
        #delete entry based of the domain provided
        self.cursor.execute("DELETE FROM passwords WHERE domain = ?", (domain,))  # domain, because it must be a tuple (1D tuple in this case)
        self.connection.commit()
        self.connection.close()

    def edit_data(self, username, password):
        #connect to the database
        self.connect()
        
        #edit both the username and password
        self.cursor.execute("UPDATE passwords SET username = ?, password = ?", (username, password))
        self.connection.commit()
        self.connection.close()
        
    def edit_username(self, username):
        #connect to the database
        self.connect()
        
        #edit the username only
        self.cursor.execute("UPDATE passwords SET username = ?", (username,))
        self.connection.commit()
        self.connection.close()
        
    def edit_password(self, password):
        #connect to the database
        self.connect()
        
        #edit the password only
        self.cursor.execute("UPDATE passwords SET password = ?", (password,))
        self.connection.commit()
        self.connection.close()
        
    def fetch_by_domain(self,domain):
        #connect to the database
        self.connect()
        
        #fetch data based of the domain provided
        self.cursor.execute("SELECT * FROM passwords WHERE domain = ?", (domain,))
        data = self.cursor.fetchall()
        return data
    
PasswordDataBase = PasswordDataBase()
print(PasswordDataBase.get_domains())



