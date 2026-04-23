# Deliverable & Source Code

In this repository, you will find the following directories:

1. /frontend-lib: TypeScript source code for the encryption library. Please read `01-FRONTEND_LIB.md` for instructions.
2. /backend: Python service code (Dockerized). Please read `02-BACKEND_PYTHON.md` for python mode. And `03-BACKEND_DOCKER.md` for dockerized backend.

# Documentation:

## Deploy service on cloud service, e.g. Vercel

For cloud deployment, please read `04-CLOUD_DEPLOYMENT.md` for the deployment strategy.

## Scenario A (Key Rotation) and

There are 2 key rotation scenarioes.

1. Data transit scenario: The data is encrypted on the client side and decrypted on the server side. Please read `05-DATA_TRANSIT_KEY_ROTATION.md`

2. Data Encryption / Encryption at rest scenario.

    - Please read `06-DATA_ENCRYPTION_KEY_ROTATION.md` for key rotation strategy when data is encrypted at rest.
    - `07-RE_ENCRYPTION_STRATEGY.md` for lazy migration and re-encryption pipeline strategy.

## Scenario B (Data Leak).

Please see `08-PII_LEAK_STRATEGY.md` for the PII leak strategy.
