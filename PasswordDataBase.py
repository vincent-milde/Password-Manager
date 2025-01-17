import sqlite3
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import hashlib
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

class PasswordDataBase ():
##################################
#                                #
#           Init for Db          #
#                                #
##################################
    def connect(self):
        #connect to the database
        self.connection = sqlite3.connect("passwords.db")
        self.cursor = self.connection.cursor()
        
    def database_exists(self):
        try:
            # Connect to the database
            self.connect()

            # Try to fetch the master password hash
            self.cursor.execute("SELECT hash FROM masterpassword")
            # If we can fetch the hash, the database exists
            result = self.cursor.fetchone()
            self.connection.close()

            if result is None:
                return False  # The masterpassword hash does not exist
            else:
                return True  # The database exists and has the master password

        except sqlite3.OperationalError:
            # If there's an OperationalError, the table or database doesn't exist
            return False
        
    def init_db(self, masterpassword):
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
            salt BLOB NOT NULL,
            hash BLOB NOT NULL
            )                 
            """)
        
        # Check if there is a salt, if not, create one
        self.cursor.execute("SELECT salt FROM masterpassword")
        result = self.cursor.fetchone()  # Fetch the first row

        if not result:  # If no salt exists, create one
            salt = os.urandom(SALT_SIZE)
            hashedpassword = hashlib.pbkdf2_hmac('sha256', masterpassword.encode(), salt, 100000)
            self.cursor.execute("INSERT INTO masterpassword (salt, hash) VALUES (?,?)", (salt, hashedpassword))
            self.connection.commit()
        else: 
            # Unpack the salt (fetchone() returns a tuple but derive key needs a byte)
            salt = result[0]
        self.key = derive_key(masterpassword, salt)
##################################
#                                #
#             Methods            #
#                                #
##################################
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
        # Connect to the database
        self.connect()
        try:
            # Encrypt the password
            encryptedPassword, iv = encrypt_data(password, self.key)
            # Attempt to insert the new entry
            self.cursor.execute(
                "INSERT INTO passwords (domain, username, password, IV) VALUES (?,?,?,?)",
                (domain, username, encryptedPassword, iv)
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"Error: The domain '{domain}' already exists in the database.")
        finally:
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
        self.connection.close()
        return data
    
    def compare_masterpassword_hash(self, provided_password):
        # Connect to the database
        self.connect()
        
        # Get the hash from the database
        self.cursor.execute("SELECT hash FROM masterpassword")
        result = self.cursor.fetchone()
        if result:
            #fetch salt for hashing
            self.cursor.execute("SELECT salt FROM masterpassword")
            temp = self.cursor.fetchone()
            self.connection.close()
            
            #convert salt,masterpassword from tuple into byte
            salt = temp[0]
            stored_password_hash = result[0]

            #hash the provided password for comparrison
            provided_password_hashed = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, 100000)
            
            if stored_password_hash == provided_password_hashed :
                return True
            else: 
                return False

        else:
            self.connection.close()
            return False  # Return None if no hash exists





