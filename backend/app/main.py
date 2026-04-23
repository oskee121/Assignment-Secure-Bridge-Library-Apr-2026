from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.db import engine, get_db
from app.crypto import decrypt_payload, blind_index, encrypt_for_storage, decrypt_from_storage, CURRENT_KEY_VERSION
import base64
import os
from dotenv import load_dotenv
load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

    # payload = {
    #   "encrypted_key": "...",
    #   "encrypted_data": "...",
    #   "iv": "...",
    #   "tag": "...",
    #   "key_version": "v1"
    # }
    # decrypt-decrypt payload steps:
    # 1. decrypt "plaintext"
    # 2. blind index the "plaintext"
    # 3. store "encrypted_data" and "blind_index" in database
@app.post("/ingest")
def ingest(payload: schemas.IngestPayload, db: Session = Depends(get_db)):
    plaintext = decrypt_payload(payload)

    index = blind_index(plaintext)

    blob, version = encrypt_for_storage(plaintext)

    record = models.SecureRecord(
        encrypted_blob=blob,
        blind_index=index,
        key_version=version,
    )

    db.add(record)
    db.commit()

    return {"status": "stored"}


@app.get("/search/{national_id}")
def search(national_id: str, db: Session = Depends(get_db)):
    index = blind_index(national_id)

    results = db.query(models.SecureRecord).filter_by(blind_index=index).all()

    return {"count": len(results)}

# get all records with pagination (decrypt all data) - temporary function for demo purpose only
@app.get("/records")
def get_records(page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    records = db.query(models.SecureRecord).all()

    output = []

    for r in records:
        plaintext = decrypt_from_storage(r.encrypted_blob, r.key_version)

        # 🔥 Lazy Migration
        if r.key_version != CURRENT_KEY_VERSION:
            new_blob, new_version = encrypt_for_storage(plaintext)

            r.encrypted_blob = new_blob
            r.key_version = new_version

            db.add(r)

        output.append({
            "id": r.id,
            "national_id": plaintext
        })

    db.commit()

    return {"results": output}


