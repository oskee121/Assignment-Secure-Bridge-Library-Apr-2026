import base64
import hashlib
import hmac
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


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

def encrypt_aes_gcm(plaintext: bytes) -> dict:
    key = load_key()
    aesgcm = AESGCM(key)

    iv = os.urandom(12)  # GCM standard
    ciphertext = aesgcm.encrypt(iv, plaintext, None)

    return {
        "iv": base64.b64encode(iv).decode(),
        "ciphertext": base64.b64encode(ciphertext).decode()
    }

def decrypt_aes_gcm(iv_b64: str, ciphertext_b64: str) -> bytes:
    key = load_key()
    aesgcm = AESGCM(key)

    iv = base64.b64decode(iv_b64)
    ciphertext = base64.b64decode(ciphertext_b64)

    return aesgcm.decrypt(iv, ciphertext, None)
