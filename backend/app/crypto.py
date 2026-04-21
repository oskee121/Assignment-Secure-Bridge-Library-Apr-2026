import base64
import os
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
import hmac
import hashlib

PRIVATE_KEY_PATH = "private.pem"
HMAC_SECRET = b"super_secret_key"

def load_private_key():
    with open(PRIVATE_KEY_PATH, "rb") as f:
        return RSA.import_key(f.read())

def decrypt_payload(encrypted_key, encrypted_data, iv, tag):
    private_key = load_private_key()
    cipher_rsa = PKCS1_OAEP.new(private_key, hashAlgo=hashlib.sha256())

    aes_key = cipher_rsa.decrypt(base64.b64decode(encrypted_key))

    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=base64.b64decode(iv))
    plaintext = cipher.decrypt_and_verify(
        base64.b64decode(encrypted_data),
        base64.b64decode(tag)
    )

    return plaintext.decode()

def blind_index(national_id: str):
    return hmac.new(HMAC_SECRET, national_id.encode(), hashlib.sha256).hexdigest()