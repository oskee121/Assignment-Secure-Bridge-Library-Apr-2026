# backend/app/migrate_keys.py

from app.db import SessionLocal
from app import models
from app.crypto import (
    decrypt_from_storage,
    encrypt_for_storage,
    get_current_key_version,
)

BATCH_SIZE = 100


def migrate_batch():
    db = SessionLocal()

    try:
        current_version = get_current_key_version()

        records = (
            db.query(models.SecureRecord)
            .filter(models.SecureRecord.key_version != current_version)
            .limit(BATCH_SIZE)
            .all()
        )

        if not records:
            print("✅ Migration complete")
            return False

        migrated_count = 0

        for r in records:
            try:
                print(
                    f"🔄 Migrating record {r.id} "
                    f"(v{r.key_version} → v{current_version})"
                )

                plaintext = decrypt_from_storage(
                    r.encrypted_blob, r.key_version
                )

                new_blob, new_version = encrypt_for_storage(plaintext)

                r.encrypted_blob = new_blob
                r.key_version = new_version

                db.add(r)
                migrated_count += 1

            except Exception as e:
                print(f"❌ Failed record {r.id}: {e}")

        db.commit()
        print(f"✔ Migrated {migrated_count}/{len(records)} records")

        return True

    except Exception as e:
        print(f"🔥 Batch failed: {e}")
        db.rollback()
        return True  # retry next loop

    finally:
        db.close()


if __name__ == "__main__":
    print("🚀 Starting key migration...")

    while True:
        has_more = migrate_batch()
        if not has_more:
            break

    print("🎉 All done!")