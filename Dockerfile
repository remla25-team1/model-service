# Build stage
FROM python:3.11-slim AS builder

WORKDIR /app

# Install git   
RUN apt-get update && \
    apt-get install -y --no-install-recommends git && \
    rm -rf /var/lib/apt/lists/*

# Install dependencies 
COPY requirements.txt .
RUN python -m pip install --upgrade pip && \
    pip install --user -r requirements.txt

# Runtime stage
FROM python:3.11-slim

WORKDIR /app

COPY src src

COPY --from=builder /root/.local /root/.local

RUN mkdir -p /app/output

# Environment variables
ENV PATH=/root/.local/bin:$PATH \
    PORT=8080 \
    HOST=0.0.0.0 \
    MODEL_DIR=/app/output \
    MODEL_VERSION=v0.0.2
  
EXPOSE ${PORT}

ENTRYPOINT ["python"]
CMD ["src/serve_model.py"]
