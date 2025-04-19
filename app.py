from flask import Flask, request, jsonify
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import statsmodels.api as sm

# ------------------------------------------
# Initialize Flask App
# ------------------------------------------
app = Flask(__name__)

# ------------------------------------------
# Prepare Dataset
# ------------------------------------------
# Data includes observed outcomes (Yobs), treatment indicator (W), and covariate (X)
data = {
    'Yobs': [137, 118, 124, 124, 120, 129, 122, 142, 128, 114,
             132, 130, 130, 112, 132, 117, 134, 132, 121, 128],
    'W':    [0, 1, 1, 1, 0, 1, 1, 0, 0, 1,
             1, 0, 0, 1, 0, 1, 0, 0, 1, 1],
    'X':    [19.8, 23.4, 27.7, 24.6, 21.5, 25.1, 22.4, 29.3, 20.8, 20.2,
             27.3, 24.5, 22.9, 18.4, 24.2, 21.0, 25.9, 23.2, 21.6, 22.8]
}
df = pd.DataFrame(data)

# ------------------------------------------
# Train scikit-learn model (for prediction)
# ------------------------------------------
# Use W (treatment) and X (covariate) to predict Yobs
X_train = df[['W', 'X']]
y_train = df['Yobs']
sk_model = LinearRegression().fit(X_train, y_train)

# ------------------------------------------
# Fit statsmodels OLS model (for ATE analysis)
# ------------------------------------------
# Add intercept column for statsmodels
df['intercept'] = 1
# Define regression model: Y = α + τ*W + β*X + ε
sm_model = sm.OLS(df['Yobs'], df[['intercept', 'W', 'X']])
sm_results = sm_model.fit()

# Display summary in console for reference
print(sm_results.summary().as_text(), flush=True)

# Extract model coefficients
alpha = sm_results.params['intercept']  # Intercept (α)
tau   = sm_results.params['W']          # Treatment effect (τ / ATE)
beta  = sm_results.params['X']          # Covariate effect (β)

# Print estimated parameters
print("\nEstimated parameters:")
print(f"Estimated α (intercept): {alpha:.4f}")
print(f"Estimated τ (treatment effect / ATE): {tau:.4f}")
print(f"Estimated β (effect of covariate X): {beta:.4f}")

# ------------------------------------------
# Define API endpoint to make predictions
# ------------------------------------------
@app.route("/predict")
def predict():
    try:
        # Get input values for W and X from query parameters
        W = float(request.args.get("W"))
        X = float(request.args.get("X"))
    except (TypeError, ValueError):
        return jsonify({"error": "Please provide valid numeric values for W and X"}), 400

    # Predict Y using the trained scikit-learn model
    y_pred = sk_model.predict([[W, X]])[0]

    # Optionally write prediction to a file
    try:
        with open("output.txt", "a") as f:
            f.write(f"Input W: {W}, X: {X} -> Predicted Y: {y_pred:.2f}\n")
        print("Successfully wrote to output.txt")
    except Exception as e:
        print("Failed to write to output.txt:", e)

    # Return prediction result as JSON
    return jsonify({
        "W": W,
        "X": X,
        "predicted_Yobs": round(y_pred, 2)
    })

# ------------------------------------------
# Define API endpoint to return ATE and CI
# ------------------------------------------
@app.route("/ate")
def get_ate():
    ate = sm_results.params['W']               # τ estimate
    p_value = sm_results.pvalues['W']          # p-value for τ
    conf_int = sm_results.conf_int().loc['W']  # 95% CI for τ

    return jsonify({
        "ATE_estimate": round(ate, 3),
        "p_value": round(p_value, 4),
        "95%_CI": [round(conf_int[0], 3), round(conf_int[1], 3)]
    })

# ------------------------------------------
# Run the Flask server
# ------------------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
