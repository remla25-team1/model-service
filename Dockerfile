FROM python:3.11-slim

WORKDIR /root/

COPY requirements.txt .

# get git
RUN apt-get update && \
	apt-get install -y --no-install-recommends git && \
	rm -rf /var/lib/apt/lists/*

RUN python -m pip install --upgrade pip && \
	pip install -r requirements.txt

# get and mount trained model
ADD https://github.com/remla25-team1/model-training/releases/download/v0.0.2/v0.0.2_Sentiment_Model.pkl \
    output/v0.0.2_Sentiment_Model.pkl.joblib
ADD https://github.com/remla25-team1/model-training/releases/download/v0.0.2/c1_BoW_Sentiment_Model.pkl \ 
	bow/c1_BoW_Sentiment_Model.pkl

COPY src src

ENTRYPOINT ["python"]
CMD ["src/serve_model.py"]
