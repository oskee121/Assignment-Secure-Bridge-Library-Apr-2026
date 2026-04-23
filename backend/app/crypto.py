import base64
import hashlib
import hmac
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import json


from dotenv import load_dotenv
load_dotenv()

# get from .env key "PRIVATE_KEY_V1_PATH"
PRIVATE_KEYS = {
    "v1": os.getenv("PRIVATE_KEY_V1_PATH")
}

# get from .env key "HMAC_KEY"
HMAC_KEY = os.getenv("HMAC_KEY")
if not HMAC_KEY:
    raise ValueError("HMAC_KEY is missing")

HMAC_KEY = HMAC_KEY.encode()


# encryption key - versions supported
KEYS = {
    "v1": base64.b64decode(os.getenv("ENCRYPTION_KEY_V1")),
    "v2": base64.b64decode(os.getenv("ENCRYPTION_KEY_V2", "")) if os.getenv("ENCRYPTION_KEY_V2") else None,
}

CURRENT_KEY_VERSION = os.getenv("ENCRYPTION_KEY_VERSION", "v1")

def load_private_key(version: str):
    # read data from file
    path = PRIVATE_KEYS[version]
    with open(path, "rb") as f:
        return RSA.import_key(f.read())


def decrypt_payload(payload):
    # payload = {
    #   "encrypted_key": "...",
    #   "encrypted_data": "...",
    #   "iv": "...",
    #   "tag": "...",
    #   "key_version": "v1"
    # }
    # decrypt payload steps:
    # 1. load private key from file (keys/v[1,2,3]/private.pem)
    # 2. decrypt "secret_key" from "encrypted_key" using "private key"
    # 3. decrypt "plaintext" from "encrypted_data" using "secret_key" >> "plaintext"
    private_key = load_private_key(payload.key_version)

    cipher_rsa = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)

    aes_key = cipher_rsa.decrypt(base64.b64decode(payload.encrypted_key))


    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=base64.b64decode(payload.iv))

    plaintext = cipher.decrypt_and_verify(
        base64.b64decode(payload.encrypted_data),
        base64.b64decode(payload.tag),
    )

    return plaintext.decode()


def blind_index(value: str):
    return hmac.new(HMAC_KEY, value.encode(), hashlib.sha256).hexdigest()


def load_key():
    # key จาก .env (base64)
    return base64.b64decode(os.environ["ENCRYPTION_KEY"])

def get_key(version: str):
    key = KEYS.get(version)
    if not key:
        raise ValueError(f"Key version {version} not found")
    return key

def encrypt_for_storage(plaintext: str):
    key = get_key(CURRENT_KEY_VERSION)

    cipher = AES.new(key, AES.MODE_GCM)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode())

    blob = {
        "ciphertext": base64.b64encode(ciphertext).decode(),
        "iv": base64.b64encode(cipher.nonce).decode(),
        "tag": base64.b64encode(tag).decode(),
    }

    return json.dumps(blob), CURRENT_KEY_VERSION

def decrypt_from_storage(blob_str: str, version: str) -> str:
    key = get_key(version)

    blob = json.loads(blob_str)

    cipher = AES.new(key, AES.MODE_GCM, nonce=base64.b64decode(blob["iv"]))

    plaintext = cipher.decrypt_and_verify(
        base64.b64decode(blob["ciphertext"]),
        base64.b64decode(blob["tag"]),
    )

    return plaintext.decode()
