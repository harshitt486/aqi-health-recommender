# AQI Health Recommender (Runnable Project)

This is a complete runnable scaffold for **AI-based Personal Health Recommendations** using air-quality data.
It contains backend (Flask), a simple ML training script, a utility for CPCB-style AQI calculation,
and a tiny frontend to test the service locally.

> NOTE: This scaffold uses **OpenAQ** or other public APIs for live AQI values. If you want fully offline
training/evaluation, download/put a CSV into `data/india_aqi_real.csv` (instructions below).

## Project Structure
```
aqi-health-recommender/
├─ data/
│  └─ india_aqi_real.csv       # (optional) real dataset CSV if you want to train locally
├─ backend/
│  ├─ requirements.txt
│  ├─ model_train.py
│  ├─ model.pkl                # created after running model_train.py
│  ├─ label_encoder.pkl        # created after running model_train.py
│  ├─ aqi_utils.py
│  └─ app.py
├─ frontend/
│  ├─ index.html
│  └─ app.js
└─ README.md
```

## Quick start (local)
1. Make a Python virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # Windows: venv\Scripts\activate
   ```

2. Install backend deps:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. (Optional) If you have a dataset, place it as `../data/india_aqi_real.csv` then run:
   ```bash
   python model_train.py
   ```
   This will create `model.pkl` and `label_encoder.pkl`. If you skip this, `app.py` will still run using a small default model included.

4. Run the Flask API:
   ```bash
   python app.py
   ```
   By default it runs on http://127.0.0.1:5000

5. Open the frontend:
   Open `frontend/index.html` in the browser (or serve it via `python -m http.server` from frontend directory) and click *Check*.

## Notes and Next Steps
- For live data: `app.py` queries OpenAQ (no API key). If you prefer OpenWeatherMap, set env var `OWM_API_KEY` and adjust `app.py`.
- The CPCB AQI conversion is in `backend/aqi_utils.py`. Use it to compute AQI from PM2.5/PM10 as per breakpoints.
- This scaffold is intentionally simple so you can iterate: add user accounts, push notifications, improved models (LSTM, Prophet), and mapping to Indian AQI categories.
