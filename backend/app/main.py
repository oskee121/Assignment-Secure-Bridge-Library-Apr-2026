from fastapi import FastAPI
from pydantic import BaseModel
from app.crypto import decrypt_payload, blind_index
import os

app = FastAPI()

DB = []

class Payload(BaseModel):
    encrypted_data: str
    encrypted_key: str
    iv: str
    tag: str
    key_version: str

@app.post("/ingest")
def ingest(data: Payload):
    plaintext = decrypt_payload(
        data.encrypted_key,
        data.encrypted_data,
        data.iv,
        data.tag
    )

    index = blind_index(plaintext)

    record = {
        "encrypted_data": os.urandom(32).hex(),  # mock randomized encryption
        "blind_index": index,
        "key_version": data.key_version
    }

    DB.append(record)

    return {"status": "stored"}

@app.get("/search/{national_id}")
def search(national_id: str):
    index = blind_index(national_id)

    results = [r for r in DB if r["blind_index"] == index]

    return {"results": results}