## Run Backend

```shell
docker build -t secure-backend .
docker run -p 8000:8000 secure-backend
```

## Run Frontend Example

```shell
const bridge = new SecureBridge(publicKey);

const payload = bridge.encrypt("1234567890123");

fetch("/ingest", {
method: "POST",
body: JSON.stringify(payload),
});
```
