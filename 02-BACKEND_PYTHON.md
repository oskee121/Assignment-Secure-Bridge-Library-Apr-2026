# To run (development mode)

Create `.env` file from `.env.example` and fill in the values.

Run this command will start the FastAPI server.

## One time: Setup virtual environment and install dependencies

```shell
cd backend
python3 -m venv venv
```

## Run the server

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
