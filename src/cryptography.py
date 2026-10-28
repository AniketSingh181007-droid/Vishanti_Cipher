import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id


MAGIC = b"check"


def derive_key(password, salt):
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=3,
        lanes=4,
        memory_cost=65536
    )

    return kdf.derive(password.encode())


def encrypt_message(message, password):
    salt = os.urandom(16)
    nonce = os.urandom(12)

    key = derive_key(password, salt)

    aes = AESGCM(key)
    ciphertext = aes.encrypt(
        nonce,
        message.encode(),
        MAGIC
    )

    return MAGIC + salt + nonce + ciphertext


def decrypt_message(payload, password):
    salt = payload[4:20]
    nonce = payload[20:32]
    ciphertext = payload[32:]

    key = derive_key(password, salt)

    aes = AESGCM(key)
    plaintext = aes.decrypt(
        nonce,
        ciphertext,
        MAGIC
    )

    return plaintext.decode()
