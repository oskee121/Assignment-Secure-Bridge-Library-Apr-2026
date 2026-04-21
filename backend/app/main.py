from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from app import models, schemas
from app.db import engine, get_db
from app.crypto import decrypt_payload, blind_index

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/ingest")
def ingest(payload: schemas.IngestPayload, db: Session = Depends(get_db)):
    plaintext = decrypt_payload(payload)

    index = blind_index(plaintext)

    record = models.SecureRecord(
        encrypted_data=payload.encrypted_data,  # store as-is (randomized)
        blind_index=index,
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