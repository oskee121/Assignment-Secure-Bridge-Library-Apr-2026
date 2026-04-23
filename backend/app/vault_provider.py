import base64
import os
import hvac
import time
from functools import lru_cache

VAULT_ADDR = os.getenv("VAULT_ADDR")
VAULT_TOKEN = os.getenv("VAULT_TOKEN")
VAULT_SECRET_PATH = os.getenv("VAULT_SECRET_PATH", "secret/data/encryption")


class VaultKeyProvider:
    def __init__(self):
        self.client = hvac.Client(url=VAULT_ADDR, token=VAULT_TOKEN)
        self._cache = None
        self._cache_expiry = 0

    def _get_secret(self):
        now = time.time()

        # cache ยังไม่หมดอายุ
        if self._cache and now < self._cache_expiry:
            return self._cache

        # fetch ใหม่จาก Vault
        print("Fetching secret from Vault...")
        secret = self.client.secrets.kv.v2.read_secret_version(
            path=VAULT_SECRET_PATH.replace("secret/data/", "")
        )

        # set cache + TTL 5 นาที
        self._cache = secret
        self._cache_expiry = now + 300  # 300 sec = 5 นาที

        return secret

    def get_current_key(self):
        secret = self._get_secret()

        data = secret["data"]["data"]
        version = data["current_version"]
        key_b64 = data[f"key_{version}"]

        return version, base64.b64decode(key_b64)

    def get_key(self, version: str):
        secret = self._get_secret()
        data = secret["data"]["data"]

        key_b64 = data.get(f"key_{version}")
        if not key_b64:
            raise ValueError(f"Key version {version} not found in Vault")

        return base64.b64decode(key_b64)

    def get_private_key(self, version: str) -> str:
        data = self._get_secret_private()
        key = data.get(version)

        if not key:
            raise ValueError(f"Private key {version} not found")

        return key


    def _get_secret_private(self):
        now = time.time()

        if hasattr(self, "_private_cache") and now < self._private_expiry:
            return self._private_cache

        secret = self.client.secrets.kv.v2.read_secret_version(
            path="private"
        )

        self._private_cache = secret["data"]["data"]
        self._private_expiry = now + 300

        return self._private_cache

    def get_blind_index_key(self) -> bytes:
        data = self._get_secret()  # reuse encryption secret
        data = data["data"]["data"]

        key_b64 = data.get("blind_index_secret")
        if not key_b64:
            raise ValueError("blind_index_secret not found in Vault")

        return key_b64.encode()
