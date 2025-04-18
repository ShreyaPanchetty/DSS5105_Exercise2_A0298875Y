from flask import Flask, request, jsonify
import joblib
import numpy as np
import logging

# Set up Flask app
app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# Load the trained model
model = joblib.load("regression_model.pkl")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        content = request.get_json()
        W = float(content.get("W"))
        X = float(content.get("X"))

        # Prepare input (must match training format: const, W, X)
        input_data = np.array([1, W, X]).reshape(1, -1)
        prediction = model.predict(input_data)[0]

        logging.info(f"Prediction made for W={W}, X={X}: {prediction}")
        return jsonify({"predicted_engagement_score": round(prediction, 2)})

    except Exception as e:
        logging.error(f"Prediction error: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
