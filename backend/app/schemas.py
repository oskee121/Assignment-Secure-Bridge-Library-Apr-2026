from pydantic import BaseModel


class IngestPayload(BaseModel):
    encrypted_data: str
    encrypted_key: str
    iv: str
    tag: str
    key_version: str

