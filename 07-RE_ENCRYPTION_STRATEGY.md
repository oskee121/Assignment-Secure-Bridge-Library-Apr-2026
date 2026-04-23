# Key Rotation Strategy

## 🪜 Step-by-step

### Step 1: เพิ่ม key ใหม่

```
ENCRYPTION_KEY_V1=...
ENCRYPTION_KEY_V2=...
ENCRYPTION_KEY_VERSION=v2
```

### Step 2: deploy

- new writes → ใช้ v2
- old data → ยังเป็น v1

### Step 3: migration (2 ทางเลือก)

#### (1) Lazy migration

- migrate ตอน read
- zero downtime
- Batch/ Scheduler ค่อย ๆ migrate

#### (2) Batch job (optional)

```
for record in batch:
    decrypt(v1)
    encrypt(v2)
    update
```

# Re-encryption Strategy for Key Rotation

| แบบ                          | complexity | เหมาะกับ            |
| ---------------------------- | ---------- | ------------------- |
| Background migration (basic) | ต่ำ        | script / cron       |
| Re-encryption pipeline       | สูง        | scale ล้าน+ records |

1. จุดสำคัญคือการ re-encrypt ต้องทำแบบ zero downtime → ไม่กระทบการใช้งานของ user หรือ program หลัก (eventually consistent)


# 1. Background Migration

**Sequence:**

```text
Cron Job / Worker
      |
      | scan DB (key_version != CURRENT)
      v
Backend Logic (reuse crypto.py)
      |
      | decrypt_from_storage(blob, old_version)
      | encrypt_for_storage(plaintext) -> new_version
      |
      v
Database UPDATE
```

**Run**

```shell
python -m app.migrate_keys
```

Output:

```text
(venv) o@Keeradit backend % python -m app.migrate_keys
DEBUG: Using DATABASE_URL: sqlite:///./data/secure.db
DEBUG: Using CURRENT_KEY_VERSION: k2
✔ Migrated 9 records
✅ Migration complete
```

หรือใช้ cron:

```cronexp
*/5 * * * * python -m app.migrate_keys
```

### ✅ ข้อดี

- ใช้ code เดิมได้เลย (decrypt_from_storage, encrypt_for_storage)
- ไม่ต้องแก้ API
- zero downtime จริง

### ❌ ข้อเสีย

- ไม่มี retry จริงจัง
- ไม่มี parallel
- ไม่มี monitoring

# 2. Re-encryption Pipeline (production grade)

**Sequence**

```shell
Scheduler
   |
   v
Producer (scan DB)
   |
   | enqueue record IDs
   v
Queue (Redis / Kafka / SQS)
   |
   v
Workers (N instances)
   |
   | fetch record by id
   | decrypt(old key)
   | encrypt(new key)
   v
Update Database
```

### ✅ ข้อดี

1. ✅ Parallel
   worker 10 ตัว = เร็วขึ้น 10 เท่า
2. ✅ Retry / Dead-letter queue

```text
      Worker fails
      |
      v
      Retry (max 3)
      |
      v
      DLQ (manual inspect)
```

3. ✅ Monitoring
   - กี่ record ที่ migrate แล้ว
   - กี่ record ที่ยังเหลือ
   - Error rate

4. ✅ Backpressure control
   จำกัด batch size
   จำกัด worker concurrency


**ข้อควรระวัง:**

1. ✅ Idempotency (สำคัญมาก)

   ต้องกันเคส:

    - record ถูก migrate ไปแล้ว
    - แต่ job retry มาอีก

    👉 Solution:

```text
if r.key_version == CURRENT_KEY_VERSION:
    skip
```

# สรุป

## ✔️ Background migration
- คือ “ขั้นต่ำที่ต้องมี”
- ใช้ได้ทันที implement ไว
- เหมาะกับ:
  - น้อยกว่า 1-3 ล้าน records (ค่าประมาณ ขึ้นอยู่กับความเร็วที่ต้องการ)
  - ไม่ต้องการความเร็ว
  - ไม่มี resource / expertise ทำ pipeline

## ✔️ Re-encryption pipeline

- คือ “version scale”
- เร็ว เพราะ parallel
- เอาไว้ตอน:
  - 5 ล้าน records ขึ้นไป หรือ background migration เริ่มมีปัญหาเรื่อง performance
- observable
