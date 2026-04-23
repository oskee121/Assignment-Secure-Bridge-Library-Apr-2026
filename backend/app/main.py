from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.db import engine, get_db
from app.crypto import decrypt_payload, blind_index, encrypt_for_storage, decrypt_from_storage
from dotenv import load_dotenv

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.post("/store")
def store(payload: schemas.StorePayload, db: Session = Depends(get_db)):
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

# NOTE: This endpoint decrypts all records and is intended for demo purposes only.
# The `page` and `per_page` params implement basic in-memory pagination.
# @app.get("/records")
# def get_records(page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
#     all_records = db.query(models.SecureRecord).all()
#
#     output = []
#     for r in all_records:
#         plaintext = decrypt_from_storage(r.encrypted_blob, r.key_version)
#
#         # Lazy key migration: re-encrypt under the current key version
#         if r.key_version != CURRENT_KEY_VERSION:
#             new_blob, new_version = encrypt_for_storage(plaintext)
#             r.encrypted_blob = new_blob
#             r.key_version = new_version
#             db.add(r)
#
#         output.append({"id": r.id, "national_id": plaintext})
#
#     db.commit()
#
#     start = (page - 1) * per_page
#     return {"results": output[start: start + per_page]}


