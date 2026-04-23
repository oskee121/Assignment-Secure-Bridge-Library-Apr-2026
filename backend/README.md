# To run (development mode)

```shell
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

To see swagger docs, open http://127.0.0.1:8000/docs in the browser.

# To generate RSA keys (private and public)

```shell
openssl genpkey -algorithm RSA -out keys/v1/private.pem -pkeyopt rsa_keygen_bits:2048
```

```shell
openssl rsa -pubout -in keys/v1/private.pem -out keys/v1/public.pem
```
