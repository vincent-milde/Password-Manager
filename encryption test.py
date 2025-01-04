from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os

# Constants
SALT_SIZE = 16  # Size of the salt
KEY_SIZE = 32   # AES 256-bit key
IV_SIZE = 16    # AES block size for CBC (128 bits)

# Deriving the key from a password using PBKDF2
def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return kdf.derive(password.encode())

# Encrypt function using AES in CBC mode
def encrypt_data(data: str, password: str) -> bytes:
    # Generate a random salt and IV
    salt = os.urandom(SALT_SIZE)
    iv = os.urandom(IV_SIZE)
    
    # Derive the key from the password
    key = derive_key(password, salt)
    
    # Pad data to be block-size compliant
    padder = padding.PKCS7(128).padder()  # AES block size = 128 bits
    padded_data = padder.update(data.encode()) + padder.finalize()
    
    # Set up AES CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    # Encrypt the padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    
    # Return the salt, IV, and ciphertext
    return salt + iv + ciphertext

# Decrypt function using AES in CBC mode
def decrypt_data(encrypted_data: bytes, password: str) -> str:
    # Extract the salt, IV, and ciphertext from the encrypted data
    salt = encrypted_data[:SALT_SIZE]
    iv = encrypted_data[SALT_SIZE:SALT_SIZE+IV_SIZE]
    ciphertext = encrypted_data[SALT_SIZE+IV_SIZE:]
    
    # Derive the key from the password
    key = derive_key(password, salt)
    
    # Set up AES CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    
    # Decrypt the data
    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    
    # Remove padding
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    
    return data.decode()

# Example usage
if __name__ == "__main__":
    password = "my_secure_password"
    plaintext = "This is a secret message."
    
    # Encrypt the data
    encrypted_data = encrypt_data(plaintext, password)
    print(f"Encrypted Data (in bytes): {encrypted_data}")
    
    # Decrypt the data
    decrypted_data = decrypt_data(encrypted_data, password)
    print(f"Decrypted Data: {decrypted_data}")
