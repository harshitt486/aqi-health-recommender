# backend/app.py
# AQI Health Recommender - AQICN integration (uses your token)
from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib, os, requests, datetime
from aqi_utils import aqi_category  # keep existing aqi_utils in backend/

# --- CONFIG: paste your token here (you provided it) ---
AQICN_TOKEN = "5e441bd3454ede843e37b6fe879317d5f120c26a"

# model files
MODEL_FILE = 'model.pkl'
LE_FILE = 'label_encoder.pkl'

app = Flask(__name__)
CORS(app)

# load model if present
model = joblib.load(MODEL_FILE) if os.path.exists(MODEL_FILE) else None
le = joblib.load(LE_FILE) if os.path.exists(LE_FILE) else None

# --------------------------
# Helper: safe HTTP GET + JSON
# --------------------------
def safe_get_json(url, params=None):
    try:
        r = requests.get(url, params=params, timeout=8)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print("HTTP/JSON error for", url, "->", str(e))
        return None

# --------------------------
# Fetch AQI from AQICN (WAQI)
# --------------------------
def fetch_aqicn_city(city="Delhi"):
    """
    Use AQICN API to get real-time AQI for 'city'.
    Returns dict: { 'aqi': int_or_none, 'pm2_5': float_or_none, 'pm10': float_or_none }
    """
    print(f"\n--- Fetching AQICN for: {city} ---")
    base = f"https://api.waqi.info/feed/{city}/"
    params = {'token': AQICN_TOKEN}
    data = safe_get_json(base, params=params)

    if data is None:
        print("AQICN: no response (network or API error).")
        return {'aqi': None, 'pm2_5': None, 'pm10': None}

    # data schema: { "status":"ok","data":{ "aqi":..., "iaqi":{ "pm25":{ "v":.. }, "pm10":{ "v":.. } }, ... } }
    status = data.get('status')
    if status != 'ok':
        print("AQICN returned non-ok status:", status, data.get('data'))
        return {'aqi': None, 'pm2_5': None, 'pm10': None}

    d = data.get('data', {})
    aqi = d.get('aqi')  # may be - or null
    iaqi = d.get('iaqi', {})

    pm25 = None
    pm10 = None

    if 'pm25' in iaqi and isinstance(iaqi['pm25'], dict):
        pm25 = iaqi['pm25'].get('v')
    if 'pm10' in iaqi and isinstance(iaqi['pm10'], dict):
        pm10 = iaqi['pm10'].get('v')

    # sometimes no iaqi fields exist — try to parse from 'dominentpol' or other structure if needed
    print("AQICN fetched:", "aqi=", aqi, "pm2.5=", pm25, "pm10=", pm10)
    return {'aqi': aqi, 'pm2_5': pm25, 'pm10': pm10}

# --------------------------
# Recommendation engine
# --------------------------
def recommend_from(aqi, risk_label, user_profile):
    recs = []
    if aqi is None:
        recs.append("AQI not available. Try again later.")
        return recs

    if aqi <= 50:
        recs.append("Air is Good. Normal activities OK.")
    elif aqi <= 100:
        recs.append("Air is Satisfactory. Normal activities OK.")
    elif aqi <= 200:
        recs.append("Air is Moderate. Sensitive people should be cautious.")
    elif aqi <= 300:
        recs.append("Air is Poor. Avoid prolonged outdoor exertion. Consider a mask.")
    elif aqi <= 400:
        recs.append("Air is Very Poor. Minimize outdoor exposure; use purifier if possible.")
    else:
        recs.append("Air is Severe. Stay indoors, use an air purifier and avoid going out.")

    if user_profile.get('has_asthma'):
        recs.append("You have asthma — keep medication nearby and avoid outdoor exertion.")
    if user_profile.get('smoker'):
        recs.append("Smoking increases risk in polluted conditions — avoid smoking and exposure.")
    return recs

# --------------------------
# API Endpoint
# --------------------------
@app.route('/current', methods=['GET'])
def current():
    city = request.args.get('city', 'Delhi')
    age = int(request.args.get('age', 25))
    has_asthma = int(request.args.get('asthma', 0))
    smoker = int(request.args.get('smoker', 0))

    # 1) primary: AQICN
    aqi_data = fetch_aqicn_city(city)

    # 2) fallback: if AQICN returns None fields, we fallback to simple default or other sources in future
    if aqi_data['aqi'] is None:
        # fallback: try OpenAQ v3 (optional) or use safe defaults
        print("AQICN returned no AQI -> using fallback defaults.")
        aqi_val = 160
        pm25_val = None
        pm10_val = None
    else:
        aqi_val = aqi_data['aqi']
        pm25_val = aqi_data['pm2_5']
        pm10_val = aqi_data['pm10']

    # Prepare features for ML (keep previous feature order)
    now = datetime.datetime.now()
    features = [
        aqi_val if aqi_val is not None else 160,
        pm25_val if pm25_val is not None else (aqi_val if aqi_val is not None else 100),
        pm10_val if pm10_val is not None else (aqi_val if aqi_val is not None else 100),
        25.0,
        60.0,
        now.hour,
        now.weekday()
    ]

    # predict risk label
    risk_label = "Medium"
    if model is not None and le is not None:
        try:
            pred = model.predict([features])[0]
            try:
                risk_label = le.inverse_transform([pred])[0]
            except Exception:
                risk_label = pred
        except Exception as e:
            print("Model prediction error:", e)
            risk_label = "Medium"

    # compute category from AQI number using your aqi_utils
    aqi_cat = aqi_category(aqi_val if aqi_val is not None else 160)
    recs = recommend_from(aqi_val if aqi_val is not None else 160, risk_label,
                          {'age': age, 'has_asthma': has_asthma, 'smoker': smoker})

    return jsonify({
        'city': city,
        'aqi': aqi_val if aqi_val is not None else 160,
        'pm2_5': pm25_val,
        'pm10': pm10_val,
        'aqi_category': aqi_cat,
        'risk': risk_label,
        'recommendations': recs
    })


if __name__ == '__main__':
    app.run(debug=True, port=5000)
