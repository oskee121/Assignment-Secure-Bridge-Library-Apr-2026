# backend/app/migrate_keys.py

from app.db import SessionLocal
from app import models
from app.crypto import decrypt_from_storage, encrypt_for_storage, CURRENT_KEY_VERSION

BATCH_SIZE = 100

def migrate_batch():
    db = SessionLocal()

    try:
        records = (
            db.query(models.SecureRecord)
            .filter(models.SecureRecord.key_version != CURRENT_KEY_VERSION)
            .limit(BATCH_SIZE)
            .all()
        )

        if not records:
            print("✅ Migration complete")
            return False

        for r in records:
            try:
                plaintext = decrypt_from_storage(r.encrypted_blob, r.key_version)

                new_blob, new_version = encrypt_for_storage(plaintext)

                r.encrypted_blob = new_blob
                r.key_version = new_version

                db.add(r)

            except Exception as e:
                print(f"❌ Failed record {r.id}: {e}")

        db.commit()
        print(f"✔ Migrated {len(records)} records")

        return True

    finally:
        db.close()


if __name__ == "__main__":
    while True:
        has_more = migrate_batch()
        if not has_more:
            break
