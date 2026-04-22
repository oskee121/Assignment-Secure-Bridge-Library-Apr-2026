import base64
import hashlib
import hmac
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

PRIVATE_KEYS = {
    "v1": "keys/v1/private.pem"
}

HMAC_SECRET = b"super_secret_key"


def load_private_key(version: str):
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
    # 1. load private key from file (keys/private.pem)
    # 2. decrypt "secret_key" from "encrypted_key" using "private key"
    # 3. decrypt "plaintext" from "encrypted_data" using "secret_key" >> "plaintext"
    private_key = load_private_key(payload.key_version)

    print(private_key)

    cipher_rsa = PKCS1_OAEP.new(private_key, hashAlgo=SHA256)

    aes_key = cipher_rsa.decrypt(base64.b64decode(payload.encrypted_key))

    print(aes_key)

    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=base64.b64decode(payload.iv))

    plaintext = cipher.decrypt_and_verify(
        base64.b64decode(payload.encrypted_data),
        base64.b64decode(payload.tag),
    )

    print(plaintext)

    return plaintext.decode()


def blind_index(value: str):
    return hmac.new(HMAC_SECRET, value.encode(), hashlib.sha256).hexdigest()