from pydantic import BaseModel


class StorePayload(BaseModel):
    encrypted_data: str
    encrypted_key: str
    iv: str
    tag: str
    key_version: str

