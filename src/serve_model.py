"""
Flask API of the tweet sentiment detection model.
"""

from flask import Flask, jsonify, request
from flasgger import Swagger
from lib_ml.preprocessing import Preprocessor
import joblib, logging

app = Flask(__name__)
swagger = Swagger(app)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

preprocessor = Preprocessor()

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

    # Transform data
    vectorizer = joblib.load("bow/c1_BoW_Sentiment_Model.pkl")
    transformed_input = vectorizer.transform([processed_tweet]).toarray()

    # Predict
    model = joblib.load('output/v0.0.2_Sentiment_Model.pkl.joblib')
    prediction = model.predict(transformed_input)[0]
    logger.info(f"Prediction result: {prediction}") # 0 is negative, 1 is positive

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
    app.run(host="0.0.0.0", port=8080, debug=True)