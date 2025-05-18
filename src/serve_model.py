"""
Flask API of the tweet sentiment detection model.
"""

import os
import joblib, logging
from flask import Flask, jsonify, request
from flasgger import Swagger
from lib_ml.preprocessing import Preprocessor
from model_downloader import download_model

# Load environment variables
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = os.environ.get("PORT", 8080)
MODEL_DIR = os.getenv("MODEL_DIR", "/app/output")
MODEL_VERSION = os.getenv("MODEL_VERSION", "v0.0.2")

# Create Flask app
app = Flask(__name__)
swagger = Swagger(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load models
download_model(f"{MODEL_VERSION}_Sentiment_Model.pkl")
download_model(f"c1_BoW_Sentiment_Model.pkl")
model = joblib.load(f'{MODEL_DIR}/{MODEL_VERSION}_Sentiment_Model.pkl')
vectorizer = joblib.load(f"{MODEL_DIR}/c1_BoW_Sentiment_Model.pkl")
preprocessor = Preprocessor()

@app.route("/version")
def version():
    """
    Get the version of the model-service.
    ---
    tags:
      - Version
    summary: Retrieve model-service version
    description: Returns the version of the model-service as injected via environment variable.
    responses:
      200:
        description: Version info retrieved successfully
        content:
          application/json:
            example:
              version: v0.0.2
    """
    # For now it gets version from enviroment. 
    return jsonify({"version": os.getenv("MODEL_VERSION", "unknown")})

@app.route("/predict", methods=['POST'])
def predict():
    """
    Predict the sentiment of a tweet. 
    ---
    consumes: 
        - application/json
    parameters:
        - name: input_data
          in: body
          description: tweet to be classified.
          required: True
          schema:
            type: object
            required: tweet
            properties:
                tweet:
                    type: string
                    example: This is an example of a tweet.
    responses:
        200:
            description: "The result of the classification: 'positive' (1) or 'negative' (0)."
    
    """
    input_data = request.get_json()
    tweet = input_data.get('tweet')

    # Preprocess tweet
    logger.info(f"Received tweet for classification: {tweet}")
    processed_tweet = preprocessor.process_item(tweet)
    logger.debug(f"Processed tweet: {processed_tweet}")

    # Predict
    transformed_input = vectorizer.transform([processed_tweet]).toarray()
    prediction = model.predict(transformed_input)[0]
    logger.info(f"Prediction result: {prediction}")

    res = {
        "result": int(prediction),
        "classifier": "Naive Bayes classifier",
        "tweet": tweet
    }

    return jsonify(res)

@app.route('/dumbpredict', methods=['POST'])
def dumb_predict():
    """
    Predict the sentiment of a tweet (dumb model: always predicts 'positive' (1)).
    ---
    consumes: 
        - application/json
    parameters:
        - name: input_data
          in: body
          description: tweet to be classified.
          required: True
          schema:
            type: object
            required: tweet
            properties:
                tweet:
                    type: string
                    example: This is an example of a tweet.
    responses:
        200:
            description: "The result of the classification: 'positive' or 'negative'."
    
    """
    input_data = request.get_json()
    tweet = input_data.get('tweet')

    return jsonify({
        "result": 1,
        "classifier": "Naive Bayes classifier",
        "tweet": tweet
    })

if __name__ == '__main__':
    app.run(host=HOST, port=PORT, debug=False)