import sqlite3
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


class PasswordDataBase:
    def __init__(self, masterpassword):
        self.connect()
        
        # Create main tables
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
        
        # Initialize master password and key
        self.cursor.execute("SELECT salt FROM masterpassword")
        result = self.cursor.fetchone()
        
        if result is None:  # No master password set
            salt = os.urandom(SALT_SIZE)
            self.cursor.execute("INSERT INTO masterpassword (salt, hash) VALUES (?, ?)", (salt, b''))
            self.connection.commit()
        else:
            salt = result[0]  # Extract salt from tuple
        
        self.key = derive_key(masterpassword, salt)
        self.connection.close()


    def connect(self):
        self.connection = sqlite3.connect("passwords.db")
        self.cursor = self.connection.cursor()

    def add_entry(self, domain, username, password):
        try:
            self.connect()
            encrypted_password, iv = encrypt_data(password, self.key)
            self.cursor.execute(
                "INSERT INTO passwords (domain, username, password, IV) VALUES (?, ?, ?, ?)",
                (domain, username, encrypted_password, iv),
            )
            self.connection.commit()
        except sqlite3.IntegrityError:
            print(f"Error: Domain '{domain}' already exists.")
        finally:
            self.connection.close()

    def delete_entry(self, domain):
        self.connect()
        self.cursor.execute("DELETE FROM passwords WHERE domain = ?", (domain,))
        self.connection.commit()
        self.connection.close()

    def edit_entry(self, domain, new_username=None, new_password=None):
        self.connect()
        if new_username:
            self.cursor.execute("UPDATE passwords SET username = ? WHERE domain = ?", (new_username, domain))
        if new_password:
            encrypted_password, iv = encrypt_data(new_password, self.key)
            self.cursor.execute(
                "UPDATE passwords SET password = ?, IV = ? WHERE domain = ?", (encrypted_password, iv, domain)
            )
        self.connection.commit()
        self.connection.close()

    def fetch_by_domain(self, domain):
        self.connect()
        self.cursor.execute("SELECT domain, username, password, IV FROM passwords WHERE domain = ?", (domain,))
        row = self.cursor.fetchone()
        self.connection.close()
        if row:
            domain, username, encrypted_password, iv = row
            decrypted_password = decrypt_data(encrypted_password, self.key, iv)
            return {"domain": domain, "username": username, "password": decrypted_password}
        return None

    def get_domains(self):
        self.connect()
        self.cursor.execute("SELECT domain FROM passwords")
        domains = [row[0] for row in self.cursor.fetchall()]
        self.connection.close()
        return domains


# Example usage:
db = PasswordDataBase("1234")
db.add_entry("google.com", "vincent", "my_secure_password")
print(db.get_domains())
print(db.fetch_by_domain("google.com"))
