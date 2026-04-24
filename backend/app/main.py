from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app import models, schemas
from app.db import engine, get_db
from app.crypto import (
    decrypt_payload,
    blind_index,
    encrypt_for_storage,
    decrypt_from_storage,
    get_current_key_version,
)
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


# NOTE: Demo-only endpoint (decrypts data)
@app.get("/records")
def get_records(page: int = 1, per_page: int = 10, db: Session = Depends(get_db)):
    all_records = db.query(models.SecureRecord).all()

    current_version = get_current_key_version()

    output = []
    migrated = 0
    failed = 0

    for r in all_records:
        try:
            plaintext = decrypt_from_storage(r.encrypted_blob, r.key_version)

            # 🔑 Lazy migration using Vault as source of truth
            if r.key_version != current_version:
                print(
                    f"♻️ Lazy migrate record {r.id} "
                    f"(v{r.key_version} → v{current_version})"
                )

                new_blob, new_version = encrypt_for_storage(plaintext)
                r.encrypted_blob = new_blob
                r.key_version = new_version

                db.add(r)
                migrated += 1

            output.append({
                "id": r.id,
                "national_id": plaintext
            })

        except Exception as e:
            print(f"❌ Failed to decrypt record {r.id}: {e}")
            failed += 1

    db.commit()

    start = (page - 1) * per_page
    paginated = output[start: start + per_page]

    return {
        "page": page,
        "per_page": per_page,
        "total": len(output),
        "migrated": migrated,
        "failed": failed,
        "results": paginated,
    }