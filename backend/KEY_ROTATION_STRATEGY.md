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
