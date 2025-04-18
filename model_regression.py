import pandas as pd
import statsmodels.api as sm
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Load data
logger.info("Loading dataset...")
data = {
    "Y_obs": [137, 118, 124, 124, 120, 129, 122, 142, 128, 114, 132, 130, 130, 112, 132, 117, 134, 132, 121, 128],
    "W":     [0,   1,   1,   1,   0,   1,   1,   0,   0,   1,   1,   0,   0,   1,   0,   1,   0,   0,   1,   1],
    "X":     [19.8, 23.4, 27.7, 24.6, 21.5, 25.1, 22.4, 29.3, 20.8, 20.2, 27.3, 24.5, 22.9, 18.4, 24.2, 21.0, 25.9, 23.2, 21.6, 22.8]
}
df = pd.DataFrame(data)

# 2. Fit regression model: Y = α + τW + βX + ε
logger.info("Fitting regression model...")
X = sm.add_constant(df[['W', 'X']])  # adds intercept term α
model = sm.OLS(df['Y_obs'], X).fit()

# 3. Output regression summarypython3 -m pip install statsmodels
logger.info("Model fitting complete. Summary:")
print(model.summary())

# 4. Save model for use in Flask later
import joblib
joblib.dump(model, 'regression_model.pkl')
logger.info("Model saved to regression_model.pkl")
