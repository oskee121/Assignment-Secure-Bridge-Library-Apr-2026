# Source Code:

In this repository, you will find the following directories:

1. /frontend-lib: TypeScript source code for the encryption library. Please read `frontend-lib/README.md` for instructions.
2. /backend: Python service code (Dockerized). Please read `DOCKER.md` for instructions.

# Documentation (README.md):

## Deploy service on cloud service, e.g. Vercel

 
## Scenario A (Key Rotation) and

There are 2 key rotation scenarioes.

1. Data transit scenario: The data is encrypted on the client side and decrypted on the server side. Please read `DATA_TRANSIT_KEY_ROTATION.md`

2. Data Encryption / Encryption at rest scenario.

   - Please read `DATA_ENCRYPTION_KEY_ROTATION.md` for key rotation strategy when data is encrypted at rest.
   - `RE_ENCRYPTION_STRATEGY.md` for lazy migration and re-encryption pipeline strategy.

## Scenario B (Data Leak).


