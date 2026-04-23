## Run Backend

```shell
# WORKED
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Docker

```shell
docker build -t secure-backend .
docker run -p 8000:8000 secure-backend
```

## Run Frontend Example

```shell
Frontend-lib
cd frontend-lib
npm install
npm run dev
```
