from cryptography.fernet import Fernet
from password_manager.settings import ENCRYPT_KEY


def encrypt_password(password, key):
    f = Fernet(ENCRYPT_KEY)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password.decode()


def decrypt_password(encrypted_password, key):
    f = Fernet(ENCRYPT_KEY)
    decrypted_password = f.decrypt(encrypted_password.encode())
    return decrypted_password.decode()
