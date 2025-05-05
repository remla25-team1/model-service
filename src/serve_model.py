"""
Flask API of the tweet sentiment detection model.
"""

import joblib, pickle
from flask import Flask, jsonify, request
from flasgger import Swagger
from lib_ml.preprocessing import Preprocessor

app = Flask(__name__)
swagger = Swagger(app)

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
    # Preprocess the input
    preprocessor = Preprocessor()
    processed_tweet = preprocessor.process_item(tweet)
    # Transform data
    cv = pickle.load(open('models/c1_BoW_Sentiment_Model.joblib', "rb"))
    processed_tweet = cv.transform([processed_tweet]).toarray()
    # Predict
    model = joblib.load('models/v0.0.2_Sentiment_Model.joblib')
    prediction = model.predict(processed_tweet)[0]

    res = {
        "result": prediction,
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