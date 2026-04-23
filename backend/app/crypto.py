import base64
import hashlib
import hmac
import json
import os

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA


from dotenv import load_dotenv
load_dotenv()

PRIVATE_KEY_PATHS = {
    "v1": os.getenv("PRIVATE_KEY_V1_PATH"),
    "v2": os.getenv("PRIVATE_KEY_V2_PATH"),
}

# get from .env key "HMAC_KEY"
HMAC_KEY = os.getenv("HMAC_KEY")
if not HMAC_KEY:
    raise ValueError("HMAC_KEY is missing")

HMAC_KEY = HMAC_KEY.encode()


# encryption key - versions supported
KEYS = {
    "k1": base64.b64decode(os.getenv("ENCRYPTION_KEY_K1", "")) if os.getenv("ENCRYPTION_KEY_K1") else None,
    "k2": base64.b64decode(os.getenv("ENCRYPTION_KEY_K2", "")) if os.getenv("ENCRYPTION_KEY_K2") else None,
    "k3": base64.b64decode(os.getenv("ENCRYPTION_KEY_K3", "")) if os.getenv("ENCRYPTION_KEY_K3") else None,
}

CURRENT_KEY_VERSION = os.getenv("ENCRYPTION_KEY_VERSION", "k1")

def load_private_key(version: str):
    path = PRIVATE_KEY_PATHS.get(version)
    if not path:
        raise ValueError(f"Private key version '{version}' not configured")
    with open(path, "rb") as f:
        return RSA.import_key(f.read())


def decrypt_payload(payload):
    private_key = load_private_key(payload.key_version)

    cipher_rsa = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)
    aes_key = cipher_rsa.decrypt(base64.b64decode(payload.encrypted_key))

    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=base64.b64decode(payload.iv))

    plaintext = cipher.decrypt_and_verify(
        base64.b64decode(payload.encrypted_data),
        base64.b64decode(payload.tag),
    )

    return plaintext.decode()


def blind_index(value: str) -> str:
    return hmac.new(HMAC_KEY, value.encode(), hashlib.sha256).hexdigest()


def get_key(version: str) -> bytes:
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
