FROM python:3.12.9-slim

WORKDIR /root/

COPY requirements.txt .

RUN apt-get update && \
	apt-get install -y git && \
	apt-get install -y curl 

RUN python -m pip install --upgrade pip && \
	pip install -r requirements.txt

# Download the pre-trained models
RUN mkdir -p models && \
    curl -L https://github.com/remla25-team1/model-training/releases/download/v0.0.2/c1_BoW_Sentiment_Model.pkl -o models/c1_BoW_Sentiment_Model.joblib && \
	curl -L https://github.com/remla25-team1/model-training/releases/download/v0.0.2/v0.0.2_Sentiment_Model.pkl -o models/v0.0.2_Sentiment_Model.joblib

COPY src src

#EXPOSE 8080 

ENTRYPOINT ["python"]
CMD ["src/serve_model.py"]
