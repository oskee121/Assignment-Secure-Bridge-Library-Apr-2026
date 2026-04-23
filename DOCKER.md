# Build and Run the Docker Container

```shell
docker build -t secure-bridge-backend .

docker run -d \
  -p 8000:8000 \
  -v $(pwd)/backend/data:/app/data \
  -v $(pwd)/backend/keys:/app/keys \
  --env-file backend/.env.docker \
  --name backend-container \
  secure-bridge-backend
```
