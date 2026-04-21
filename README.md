## Run Backend

```shell
source venv/bin/activate # IMPORTANT: use `venv\Scripts\activate` on Windows
pip install -r requirements.txt
pip install -r requirements.txt
uvicorn app.main:app --reload
```

(or) (unused)

```shell
docker build -t secure-backend .
docker run -p 8000:8000 secure-backend
```

## Run Frontend Example

```shell
Frontend-lib
cd frontend-lib
npm install
npm run build
```

(unused)

```shell
const bridge = new SecureBridge(publicKey);

const payload = bridge.encrypt("1234567890123");

fetch("/ingest", {
method: "POST",
body: JSON.stringify(payload),
});
```
