# Data Enxcryption at Rest

## Core Idea

- key_version อยู่ใน DB → ใช้เลือก key ตอน decrypt
- decrypt_from_storage(blob, version) → decrypt ตาม version
- encrypt_for_storage() → ใช้ CURRENT_KEY_VERSION
- Lazy migration ตอน read (/records)

**Concept:** “Key Versioning + Lazy Migration” แบบ zero downtime

## Phase 1: ก่อน Rotate (Current = k1)

```text
Client (frontend-lib)
    |
    | 1. Encrypt (public.pem v1)
    | 2. Send payload (key_version=v1)
    v
Backend (FastAPI)
    |
    | 3. decrypt_payload()  -> ใช้ RSA private v1
    | 4. encrypt_for_storage() -> ใช้ DEK = k1
    |
    v
Database
    - encrypted_blob (AES-GCM)
    - key_version = "k1"
```

**จุดสำคัญ:**

- ทุก record = k1
- system stable
- CURRENT_KEY_VERSION = k1

## Phase 2: Rotate Key (Current = k2)

ระหว่าง Rotate (k1 → k2)

### Steps

**Step 0**: Deploy config ใหม่ (no downtime)

```text
backend/.env
ENCRYPTION_KEY_VERSION = k2
```

และมี:

```text
KEYS = { k1, k2, k3 }
```

Sequence diagram (Mixed State)

```text
                ┌──────────────────────────────┐
                │   Backend (FastAPI)          │
                │ CURRENT_KEY = k2             │
                └────────────┬─────────────────┘
                             │
        ┌────────────────────┼────────────────────┐
        │                    │                    │
        │                    │                    │
   Old Record           New Write           Read + Lazy Migration
   (k1)                 (k2)                (/records)
        │                    │                    │
        v                    v                    v

    Database            Database             Backend Logic
    --------            --------             ----------------
    key_version=k1      key_version=k2       decrypt_from_storage(blob, version)
                                                  |
                                                  v
                                             plaintext
        
                                             IF version != k2:
                                                 encrypt_for_storage()
                                                 UPDATE record → k2
```

**อธิบาย behavior**

- New records ✅ Write ใหม่ (k2)
- ใช้ encrypt_for_storage() → ได้ k2

**Read** (lazy migration)

จาก Code python:

```python
plaintext = decrypt_from_storage(r.encrypted_blob, r.key_version)

if r.key_version != CURRENT_KEY_VERSION:
    new_blob, new_version = encrypt_for_storage(plaintext)
    r.encrypted_blob = new_blob
    r.key_version = new_version
```

```text
“Read → Decrypt → Re-encrypt → Save”
```

คือถ้าเจอ record ที่ยังเป็น k1 (version != CURRENT_KEY_VERSION) → จะทำการ re-encrypt ด้วย k2 และ update record นั้นทันที

**Insight**

ระบบรู้ว่าใช้ key ไหน decrypt ยังไง?

👉 จาก field `key_version` (ใน DB)

แล้วทำการ:

```text
decrypt_from_storage(blob, version)
```

ตาม key version ที่ระบุใน record นั้นๆ

### State during migration

| Record | key_version | status          |
| ------ | ----------- | --------------- |
| A      | k1          | ยังไม่ถูกอ่าน   |
| B      | k1          | pending migrate |
| C      | k2          | migrated        |
| D      | k2          | new data        |

system อยู่ใน mixed-key state ได้แบบปลอดภัย

## Phase 3: หลัง Rotate (Current = k2)

เมื่อเวลาผ่านไป:

```text
All records → k2
```

Sequence:

```text
Client
   |
   v
Backend
   |
   | decrypt_from_storage(blob, "k2")
   | (no migration needed)
   v
Database (all k2)
```

หลังจากทุก record ถูก migrate เป็น k2 แล้ว

### Cleanup
- remove ENCRYPTION_KEY_K1
- remove private key v1
- remove frontend public.pem v1

หรือเก็บไว้เป็น fallback (recommended)
