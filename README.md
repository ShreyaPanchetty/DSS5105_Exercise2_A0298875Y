# 📊 DSS5105 Exercise 2 – Causal Inference + Flask API + Docker

## Overview
This project applies the Rubin Causal Model to estimate the Average Treatment Effect (ATE) using simulated corporate engagement data. The trained model is deployed via a Flask API and containerized with Docker for reproducibility.

---

## Project Components

### `app.py`
- A Flask API that serves:
  - `/predict`: Predicts stakeholder engagement score based on treatment (W) and spending (X).
  - `/ate`: Returns the estimated ATE, p-value, and confidence interval from statsmodels.

### `requirements.txt`
Lists dependencies: Flask, NumPy, pandas, scikit-learn, statsmodels.

### `Dockerfile`
Defines a lightweight Python environment with all packages pre-installed. Enables seamless deployment in Codespaces or locally.

---

##  Docker Instructions

### Build the Image
```docker build -t my-api .```

### Run the Container
```docker run -p 7000:7000 my-api```

### Prediction Endpoint
```
curl "http://localhost:7000/predict?W=1&X=20"
```
**Response:**
```json
{
  "W": 1.0,
  "X": 20.0,
  "predicted_Yobs": 117.16
}
```

📸 Screenshot:
![Prediction Endpoint](./Screenshot_2025-04-19_at_9.30.22_PM.png)

---

### 📉 ATE Endpoint
```bash
curl http://localhost:7000/ate
```
**Response:**
```json
{
  "ATE_estimate": -9.106,
  "p_value": 0.0004,
  "95%_CI": [-13.438, -4.773]
}
```
![ATE Endpoint](./Screenshot_2025-04-19_at_9.31.28_PM.png)

---

## 📊 Regression Summary Output

### Terminal Output when Flask Starts:

![Regression Summary](./Screenshot_2025-04-19_at_9.25.26_PM.png)

### Docker Container Output:

![Docker Run Output](./Screenshot_2025-04-19_at_9.26.25_PM.png)

---

## Files Summary

- `app.py` – Flask API for predictions and ATE
- `requirements.txt` – Python packages
- `Dockerfile` – Container setup
- `output.txt` – API usage log
- `results.txt` – Model coefficients, statistical analysis, and causal interpretation

---

