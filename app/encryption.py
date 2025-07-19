"""
This file deals with key and encryption and decryption and uses AES
this method in this file is learned from w3school and some online forums
"""

from cryptography.fernet import Fernet
import os

encryption_keyfile = "data/encryption.key"

def create_key():
    """create the key"""
    encryption_key = Fernet.generate_key()
    with open(encryption_keyfile, "wb") as encryption_file:
        encryption_file.write(encryption_key)

def load_key_file():
    """this function loads the encryption key and creates if it doesn't exist"""
    if not os.path.exists(encryption_keyfile):
        create_key()
    with open(encryption_keyfile, "rb") as key_file:
        return key_file.read()

ENCRYPT_CIPHER = Fernet(load_key_file()) # w3school

def encrypt_data(data_to_encrypt):
    """now encrypt the data using encrypt method"""
    return ENCRYPT_CIPHER.encrypt(data_to_encrypt)

def decrypt_data(security_token):
    """this function is for decryption"""
    return ENCRYPT_CIPHER.decrypt(security_token)
