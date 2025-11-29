🌍 AQI Health Recommender (AI + Live AQI + ML + Flask + JS)

A real-time Air Quality Index (AQI) health recommendation system using live AQICN API data, machine learning, and personal health factors to generate personalized health safety advice.

🚀 Features
🌐 Live AQI Retrieval

Uses AQICN API (token-based)

Supports all Indian cities

Shows AQI, PM2.5, PM10

🧠 ML-Based Risk Prediction

Predicts user health risk

Inputs:

AQI

PM2.5

PM10

Temperature

Humidity

Hour

Day of Week

Age / Asthma / Smoking history

🩺 Personalized Health Recommendations

Age relevance

Asthma sensitivity

Smoking sensitivity

🖥️ Full Stack Project

Flask backend

HTML/CSS/JavaScript frontend

Complete API + UI integration

Deployment-ready

📦 Project Structure
aqi-health-recommender/
│
├── backend/
│   ├── app.py
│   ├── model.pkl
│   ├── label_encoder.pkl
│   ├── aqi_utils.py
│   ├── requirements.txt
│   ├── render.yaml
│
├── frontend/
│   ├── index.html
│   ├── app.js
│   ├── style.css
│
├── README.md

▶ Running Locally
Backend
cd backend
pip install -r requirements.txt
python app.py


Runs at:

http://127.0.0.1:5000

Frontend

Open:

frontend/index.html

🔗 API Example
Request:
/current?city=Kanpur&age=24&asthma=0&smoker=0

Example Response:
{
  "city": "Kanpur",
  "aqi": 132,
  "pm2_5": 132,
  "pm10": 86,
  "aqi_category": "Moderate",
  "risk": "Medium",
  "recommendations": [
    "Air is Moderate. Sensitive people should be cautious."
  ]
}

🌐 Deployment
Backend (Render)

Connect GitHub repo

Add environment variable:

AQICN_TOKEN=your_api_token


Render auto-deploys your Flask app

Frontend (Vercel / Netlify)

Deploy frontend/ folder

Replace backend URL in app.js with Render URL

🧪 Future Improvements

24-hour AQI graph

7-day ML prediction

Weather + AQI combined health risk

Android/Ios app version

Notification alerts for bad AQI

🧑‍💻 Author

Harshit Kumar Tiwari
B.Tech — Computer Science (Cyber Security)

📧 harshittiwari486@gmail.com

🔗 LinkedIn: https://www.linkedin.com/in/harshit-tiwari-8206b1329
