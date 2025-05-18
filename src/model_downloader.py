import os
import requests

MODEL_DIR = os.getenv("MODEL_DIR", "/app/output")
MODEL_VERSION = os.getenv("MODEL_VERSION", "v0.0.2")

def download_model(model_name):
    """
    Download the specified model file from the GitHub release if it is not already cached locally.
    """
    model_path = f"{MODEL_DIR}/{model_name}"
    if not os.path.exists(model_path):
        print(f"Downloading model version {MODEL_VERSION}...")
        url = "https://github.com/remla25-team1/model-training/releases/download"
        r = requests.get(f"{url}/{MODEL_VERSION}/{model_name}")
        r.raise_for_status()
        with open(model_path, "wb") as f:
            f.write(r.content)
    else:
        print(f"Using cached model at {model_path}")

if __name__ == "__main__":
    # For local testing
    download_model(f"{MODEL_VERSION}_Sentiment_Model.pkl")
    download_model(f"c1_BoW_Sentiment_Model.pkl")