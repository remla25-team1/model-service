"""
Flask API of the tweet sentiment detection model.
"""

import joblib
from flask import Flask, jsonify, request
from flasgger import Swagger

# from lib_ml.preprocessing import prepare  
# import model from an accessible location with a public link

app = Flask(__name__)
swagger = Swagger(app)

@app.route("/", methods=["GET"])
def index():
    return "REST API for model-service"


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
            description: "The result of the classification: 'positive' or 'negative'."
    
    """
    input_data = request.get_json()
    tweet = input_data.get('tweet')
    processed_tweet = prepare(tweet)
    model = joblib.load('output/model.joblib')
    prediction = model.predict(processed_tweet)[0]

    res = {
        "result": prediction,
        "classifier": "decision tree",
        "tweet": tweet
    }
    print(tweet)

    return jsonify(res)


@app.route('/dumbpredict', methods=['POST'])
def dumb_predict():
    """
    Predict the sentiment of a tweet (dumb model: always predicts 'positive').
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
        "result": "Positive",
        "classifier": "decision tree",
        "tweet": tweet
    })


if __name__ == '__main__':
    # clf = joblib.load('output/model.joblib')
    app.run(host="0.0.0.0", port=8080, debug=True)