import os

from cryptography.fernet import Fernet


_secret_key = os.environ.get("APP_SECRET_KEY")
if not _secret_key:
    raise RuntimeError("APP_SECRET_KEY environment variable is required")

_fernet = Fernet(_secret_key.encode() if isinstance(_secret_key, str) else _secret_key)


def encrypt(plaintext: str) -> str:
    if plaintext is None:
        return None
    return _fernet.encrypt(plaintext.encode()).decode()


def decrypt(ciphertext: str) -> str:
    if ciphertext is None:
        return None
    return _fernet.decrypt(ciphertext.encode()).decode()
