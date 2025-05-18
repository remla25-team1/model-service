# Model Service

This is a standalone microservice that serves a sentiment analysis model via a REST API.

This service downloads the sentiment analysis model at startup and caches it in a mounted volume so it does not have to download the model every time the container restarts.

## Running the Service with Docker

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) installed on your system

### Clone the Repository

Clone the **model-service** repository from GitHub (e.g., using SSH):

```bash
git clone git@github.com:remla25-team1/model-service.git
cd model-service
```

### Create a folder for cached models

This folder will store the downloaded model files persistently on your host.

```bash
mkdir -p ./cached_model
```

### Build the Docker Image

```bash
docker build -t model-service .
```

### Run the Container  

Mount the cached model folder to persist downloaded model files:

```bash
docker run -p 8080:8080 -v $(pwd)/cached_model:/app/output model-service
```

### Verify Model Caching

- **First run:** You should see logs indicating the model is being downloaded.
- **Stop the container:** Press ```CTR+C``` or run:
```bash
docker ps            # find container ID
docker stop <ID>     # stop the container
```
- **Check the cache folder:** Inspect the ```cached_model``` folder on your host machine. It should now contain model files
- **Restart the container with the same volume:**
```bash
docker run -p 8080:8080 -v $(pwd)/cached_model:/app/output model-service
```
- **On subsequent starts:** The logs should show the model loading from cache instead of downloading again.

### API Documentation with Swagger

Once the container is running, you can explore and test the API via the Swagger UI.

Open your browser and go to:

```bash
http://localhost:8080/apidocs
```

There you can:
- See available endpoints
- View request/response formats
- Test endpoints