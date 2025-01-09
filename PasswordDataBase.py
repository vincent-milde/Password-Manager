import sqlite3
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

'''
Create a Database that stores a domain with a username and password bound to it

create methods to: 
    add/delete passwords
    fetch/edit Data
    search data by domain
''' 

##################################################
#
#             Provided by Examples
#
##################################################

# Constants
SALT_SIZE = 16  # Size of the salt
KEY_SIZE = 32   # AES 256-bit key
IV_SIZE = 16    # AES block size for CBC (128 bits)

# Deriving the key from a password using PBKDF2
def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Encrypt function using AES in CBC mode
def encrypt_data(data, key):

    # Generate a random IV
    iv = os.urandom(IV_SIZE)

    # Pad data to be block-size compliant
    padder = padding.PKCS7(128).padder()  # AES block size = 128 bits
    padded_data = padder.update(data.encode()) + padder.finalize()
    
    # Set up AES CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Encrypt the padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    return ciphertext, iv
    

# Decrypt function using AES in CBC mode
def decrypt_data(encrypted_data, key, iv):
    # Extract the salt, IV, and ciphertext from the encrypted data
    ciphertext = encrypted_data
    
    # Set up AES CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    
    return data.decode()





##################################################
#
#                 End of Examples
#
##################################################
password = "1234"

class PasswordDataBase ():
    def __init__(self, masterpassword):
        #connect to the database
        self.connect()
        #Main Table/format for storing the data
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            domain TEXT NOT NULL UNIQUE,
            username TEXT NOT NULL,
            password BLOB NOT NULL,
            IV BLOB NOT NULL                                   
            )               
            """)
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS masterpassword (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            salt BLOB NOT NULL     
            )                 
            """)
        
        # Check if there is a salt, if not, create one
        self.cursor.execute("SELECT salt FROM masterpassword")
        if not self.cursor.fetchone():                  #fetch the first row and check if it's empty
            salt =os.urandom(16)
            self.cursor.execute("INSERT INTO masterpassword (salt) VALUES (?)", (salt,))
            self.connection.commit()
        else: 
            salt = self.cursor.fetchone()
        
        print(salt)
        self.key = derive_key(masterpassword, salt)

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
        encryptedPassword, iv = encrypt_data(password, self.key)
        self.cursor.execute("INSERT INTO passwords (domain, username, password, IV) VALUES (?,?,?,?)", (domain, username, encryptedPassword, iv))
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
    
PasswordDataBase = PasswordDataBase("1234")
PasswordDataBase.add_entry("google.com", "vincent", "Tye" )
print(PasswordDataBase.get_domains())



