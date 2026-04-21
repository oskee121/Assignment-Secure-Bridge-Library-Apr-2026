import base64
import hashlib
import hmac
from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

PRIVATE_KEYS = {
    "v1": "private.pem"
}

HMAC_SECRET = b"super_secret_key"


def load_private_key(version: str):
    path = PRIVATE_KEYS[version]
    with open(path, "rb") as f:
        return RSA.import_key(f.read())


def decrypt_payload(payload):
    private_key = load_private_key(payload.key_version)

    cipher_rsa = PKCS1_OAEP.new(private_key, hashAlgo=hashlib.sha256())

    aes_key = cipher_rsa.decrypt(base64.b64decode(payload.encrypted_key))

    cipher = AES.new(aes_key, AES.MODE_GCM, nonce=base64.b64decode(payload.iv))

    plaintext = cipher.decrypt_and_verify(
        base64.b64decode(payload.encrypted_data),
        base64.b64decode(payload.tag),
    )

    return plaintext.decode()


def blind_index(value: str):
    return hmac.new(HMAC_SECRET, value.encode(), hashlib.sha256).hexdigest()