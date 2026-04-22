from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import engine, get_db
from app.crypto import decrypt_payload, blind_index

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/ingest")
def ingest(payload: schemas.IngestPayload, db: Session = Depends(get_db)):
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
    # 4. blind index the "plaintext"
    # 5. store "encrypted_data" and "blind_index" in database
    plaintext = decrypt_payload(payload)

    index = blind_index(plaintext)

    record = models.SecureRecord(
        encrypted_data=payload.encrypted_data,  # store as-is (randomized)
        blind_index=index,
        raw_data_for_demo_only=plaintext,
        key_version=payload.key_version,
    )

    db.add(record)
    db.commit()

    return {"status": "stored"}


@app.get("/search/{national_id}")
def search(national_id: str, db: Session = Depends(get_db)):
    index = blind_index(national_id)

    results = db.query(models.SecureRecord).filter_by(blind_index=index).all()

    return {
        "count": len(results),
        "results": [
            {
                "id": r.id,
                "encrypted_data": r.encrypted_data,
                "key_version": r.key_version,
            }
            for r in results
        ],
    }