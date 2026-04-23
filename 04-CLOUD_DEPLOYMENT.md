# Architecture

```text
Frontend (client)
   ↓
CloudFront (CDN)
   ↓
API Gateway
   ↓
ECS Fargate / Lambda (frontend-lib)
   ↓
Backend (FastAPI / Node)
   ↓
Secrets Manager / KMS / DB
```

# Frontend-lib: Vercel (Node, npm)

## วิธี deploy:

```shell
npm run build
```

1. push GitHub
2. connect กับ Vercel
3. Setup Enironment Variables บน Vercel
4. Build & Deploy บน Vercel

# Backend (FastAPI) – Deploy บน AWS

วิธีที่เหมาะสุด: ECS Fargate (Docker)

1. Build Docker image

```shell
docker build -t secure-bridge-backend .
```

2. Push ไป ECR

```shell
aws ecr create-repository --repository-name secure-bridge

docker tag secure-bridge-backend:latest <ECR_URI>
docker push <ECR_URI>
```

3. Run บน ECS Fargate

- ใช้ Task Definition

- ใส่ environment:

```shell
VAULT_ADDR
```

- เก็บ secret ใน AWS Secrets Manager:

```json
{
"HMAC_KEY": "...",
"VAULT_TOKEN": "..."
}
```

- ECS Task Definition

```json
"secrets": [
  {
    "name": "HMAC_KEY",
    "valueFrom": "arn:aws:secretsmanager:xxx:secret:hmac"
  },
  {
    "name": "VAULT_TOKEN",
    "valueFrom": "arn:aws:secretsmanager:xxx:secret:vault"
  }
]
```

- attach IAM role (สำคัญมาก)

**Security Best Practice**

- ใช้:
    - AWS Secrets Manager
    - AWS KMS

```json
"Action": [
  "secretsmanager:GetSecretValue"
]
```

**Logging strategy**

- log → ห้าม log decrypted data
- เปิด:
  - structured logging
  - log masking
  
**Expose API**

- ใช้:
    - Amazon API Gateway หรือ ALB (Application Load Balancer)

