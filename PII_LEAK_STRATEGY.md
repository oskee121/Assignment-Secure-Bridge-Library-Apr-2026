# PII Data Leak Incident handling

## 1. Immediate Actions

1. Stop the bleeding (หยุดการรั่ว)

    - ปิด logging ของ field ที่เป็น PII ทันที (hotfix)
    - Redeploy service ASAP
    - Revoke access ที่ไม่จำเป็นกับ log system (IAM tightening)

2. Assess impact

    - Query logs ย้อนหลัง 24-48 ชม. (แล้วแต่ว่าหลุดมานานแค่ไหน):
      - มีข้อมูลหลุดกี่ record?
      - ดูว่าถูก access ไปหรือยัง (audit log)
    - ตรวจว่าเป็นแค่ internal exposure หรือ external breach

3. Contain access

    - จำกัดสิทธิ์การเข้าถึง log:
      - remove broad roles เช่น *Viewer
      - enforce least privilege
    - ถ้าใช้ cloud logging:
      - audit access ใน Amazon CloudWatch หรือ Google Cloud Logging

4. Notify stakeholders

   - แจ้ง Security / Compliance / Legal
   - ถ้ามี regulatory impact → prepare breach notification (PDPA/GDPR style)

## 2. Remediation (แก้ของที่หลุดไปแล้ว)

1. Delete / Redact logs

    - ใช้ log retention + delete API ลบ logs ที่มี PII ออก
    - ถ้าลบไม่ได้ทั้งหมด:
      - encrypt logs (ย้อนหลัง)
      - move ไป secure bucket + restrict access

2. Rotate sensitive data (ถ้าจำเป็น)

    - กรณีนี้เป็น National ID เปลี่ยนไม่ได้ จึงต้อง:
      - Flag impacted users
      - เพิ่ม Monitoring fraud
    - Rotate keys ที่เกี่ยวข้อง (ถ้ามี) เผื่อมี correlation leak

3. Audit trail

   - เก็บ evidence:
     - ใคร access logs
     - access จาก IP ไหน
   - สำคัญมากสำหรับ compliance

## 3. Prevention (ป้องกันไม่ให้เกิดซ้ำ)

### A. Code-level controls

1. Secure logging wrapper. Enforce rule:

```javascript
log_safe(data)
```

- ตัวอย่าง function log_safe จะ strip PII อัตโนมัติ

2. Structured logging + Allowlist (Code review focus)

   - ห้าม log object ทั้งก้อน (เช่น logger.info(user))
   - Code review checklist: ต้องมี log_safe ครอบทุกที่ที่ log PII

### B. Platform-level controls

1. Log scanning / DLP

   - ใช้ regex detect:
     - National ID pattern

2. Access control

    - Least Privilege: Developer ไม่ควรมีสิทธิ์เข้าถึง production logs (RBAC/IAM tightening)
    - ถ้าจำเป็นต้องดู Production log จริงๆ ให้ใช้ Just-in-time access (temporary access)
    - Audit log ทุกอย่าง
      - ใครเปิด log
      - เปิดเมื่อไหร่
      - ดูอะไรไปบ้าง

3. Encryption everywhere

   - logs ต้อง:
     - at-rest encryption
     - optionally field-level encryption

4. Short retention for sensitive logs

   - เช่น:
     - Debug logs: 7 วัน
     - Production logs: 30 วัน

### C. Process-level controls

1. Secure coding guideline

   - Treat/Assume logs are hostile environment
     - คิดเสมอว่า logs เหมือน public data
     - logs อาจถูก access โดย attacker → ห้าม log PII เลยดีกว่า

2. Code review checklist

   - PR ต้องมี:
     - check logging statements

3. Automated scanning in CI/CD

   - detect:
     - print(user.national_id)
     - unsafe logging

4. Incident playbook

   - มี runbook เพื่อใช้ตอนเจอปัญหา

