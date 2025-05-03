FROM python:3.11-slim
# Note: previous 3.12-slim image doesn't contain pre-compiled wheels to do machine learning,
#       though could manually add those toolkits, it's unbearably slow to build

# get git
RUN apt-get update && \
	apt-get install -y --no-install-recommends git && \
	rm -rf /var/lib/apt/lists/*

WORKDIR /root/
COPY requirements.txt .

RUN python -m pip install --upgrade pip &&\
	pip install -r requirements.txt

# get and mount trained model
ADD https://github.com/remla25-team1/model-training/releases/download/v0.0.2/v0.0.2_Sentiment_Model.pkl \
    output/model.joblib

ADD https://github.com/remla25-team1/model-training/releases/download/v0.0.2/c1_BoW_Sentiment_Model.pkl \ 
	bow/c1_BoW_Sentiment_Model.pkl

COPY src src

#EXPOSE 8080 

ENTRYPOINT ["python"]
CMD ["src/serve_model.py"]
