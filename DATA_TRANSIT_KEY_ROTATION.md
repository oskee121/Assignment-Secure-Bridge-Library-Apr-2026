# Data transition key rotation

## Backend

เพิ่ม key ใหม่ (v2) ใน config ()

## Frontend

Update config ใหม่ที่ฝั่ง Frontend (no downtime)

```text
VERIFICATION_SERVICE_PUBLIC_KEY=./keys/v2/public.pem
VERIFICATION_SERVICE_PUBLIC_KEY_VERSION=v2
```
