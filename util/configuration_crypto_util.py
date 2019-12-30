import io

from cryptography.fernet import Fernet
from configparser import ConfigParser
from ..config import Config

file = open(Config.SECRET_KEY_LOCATION, 'rb')
key = file.read()
file.close()


def encrypt_configuration_file(input_file_path, destination_file_path):
    with open(input_file_path, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted = fernet.encrypt(data)

    with open(destination_file_path, 'wb') as f:
        f.write(encrypted)


def decrypt_configuration_file(input_file_path):
    with open(input_file_path, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    decrypted = fernet.decrypt(data)
    buf = io.StringIO(io.BytesIO(decrypted).read().decode('UTF-8'))

    config = ConfigParser()
    config.read_file(buf)
    return config

