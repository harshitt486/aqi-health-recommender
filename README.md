🌍 AQI Health Recommender — AI-Based Live Air Quality Health Assistant










A real-time Air Quality Index (AQI) Health Recommender that uses:

Live AQICN API (real-time AQI, PM2.5, PM10)

Machine Learning model to predict health risk

User factors (age, asthma, smoker)

Flask backend API

HTML/CSS/JS frontend

It provides personalized health recommendations based on real-time pollution levels for any Indian city.

📑 Table of Contents

✨ Features

📦 Project Structure

⚙️ Setup (Local)

🔑 Environment Variables

📡 API Usage

🌐 Deployment Guide

🚀 Future Improvements

👨‍💻 Author

✨ Features
🌐 Live AQI & Pollution Data

Uses AQICN API (Token required)

Returns:

AQI

PM2.5

PM10

AQI Category (Good → Severe)

🧠 ML-Based Health Risk Prediction

Predicts: Low / Medium / High risk

Based on:

AQI

PM2.5

PM10

Hour of day

Day of week

Temperature

Humidity

🩺 Personalized Health Recommendations

If user has asthma, gives extra warnings

If smoker, increases risk

General public recommendations based on AQI category

🖥️ Full Stack Project

Backend: Flask + Python

Frontend: HTML + CSS + JavaScript

ML Model: Scikit-learn

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
├── data/
│   ├── (optional synthetic / CSV data)
│
└── README.md

⚙️ Setup (Local)
1️⃣ Clone Repository
git clone https://github.com/harshitt486/aqi-health-recommender
cd aqi-health-recommender/backend

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Set Your AQICN Token

(Required for live AQI data)

Windows:
set AQICN_TOKEN=your_token_here

Mac/Linux:
export AQICN_TOKEN=your_token_here

4️⃣ Run Backend
python app.py


Runs at:

http://127.0.0.1:5000

5️⃣ Run Frontend

Open in your browser:

frontend/index.html

🔑 Environment Variables
Variable	Description
AQICN_TOKEN	Your real-time AQI API token from api.waqi.info

Get your token from:
👉 https://aqicn.org/data-platform/token/

📡 API Usage
Endpoint:
GET /current?city={city}&age={age}&asthma=0|1&smoker=0|1

Example:
http://127.0.0.1:5000/current?city=Kanpur&age=24&asthma=0&smoker=0

Sample Response
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

🌐 Deployment Guide
🔵 Backend — Render Deployment

Push this repo to GitHub

Visit https://render.com

Create new Web Service

Connect repo

Set environment variable:

AQICN_TOKEN=your_token_here


Render auto-installs using:

pip install -r requirements.txt


Start command:

gunicorn app:app


You will get a live URL like:

https://aqi-backend.onrender.com

🟣 Frontend — Vercel Deployment

Go to https://vercel.com

New Project → Select Repo

Choose frontend/ folder

Deploy

Update app.js with backend URL:

const url = "https://aqi-backend.onrender.com/current?...";

🚀 Future Improvements

📊 AQI Graphs (24 hours / 7 days)

📱 Mobile App (React Native / Flutter)

🔔 Push Notifications for high pollution

🌡️ Weather + AQI combined risk score

🧬 Train ML model on real CPCB data

🏙️ Auto city detection via geolocation

👨‍💻 Author

Harshit Kumar Tiwari
B.Tech — Computer Science (Cyber Security)

📍 Noida, India
📧 harshittiwari486@gmail.com

🔗 Linkedin: https://www.linkedin.com/in/harshit-tiwari-8206b1329

⭐ If you like this project

Please ⭐ star the repo — it inspires additional improvements!
