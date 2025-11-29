# Trains a RandomForest model on a provided CSV file (india_aqi_real.csv)
# If no dataset is present, this script creates a small synthetic CSV to demonstrate training.

import os
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

DATA_PATH = os.path.join('..','data','india_aqi_real.csv')
OUT_MODEL = 'model.pkl'
OUT_LE = 'label_encoder.pkl'

def create_synthetic(path):
    import random, pandas as pd
    rows = []
    for d in range(300):
        pm25 = max(5, random.gauss(100,60))
        pm10 = max(10, pm25 + random.gauss(20,40))
        aqi = int(max(pm25, pm10))
        temp = random.uniform(15,40)
        hum = random.uniform(20,90)
        hour = random.randint(0,23)
        day = random.randint(0,6)
        rows.append([pd.Timestamp.now(), pm25, pm10, aqi, temp, hum, hour, day])
    df = pd.DataFrame(rows, columns=['timestamp','pm2_5','pm10','aqi','temperature','humidity','hour','day'])
    df.to_csv(path, index=False)
    return df

if not os.path.exists(DATA_PATH):
    print("No real dataset found at", DATA_PATH)
    print("Creating a small synthetic dataset for demo purposes.")
    df = create_synthetic(DATA_PATH)
else:
    df = pd.read_csv(DATA_PATH)
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    else:
        df['timestamp'] = pd.to_datetime(df.iloc[:,0], errors='coerce')

df['hour'] = df['timestamp'].dt.hour
df['day'] = df['timestamp'].dt.dayofweek

def aqi_to_risk(aqi):
    if aqi <= 100: return 'Low'
    if aqi <= 200: return 'Medium'
    return 'High'

df['risk'] = df['aqi'].apply(aqi_to_risk)

features = ['aqi','pm2_5','pm10','temperature','humidity','hour','day']
X = df[features].apply(pd.to_numeric, errors='coerce')
X = X.fillna(X.mean())
y = df['risk']

from sklearn.preprocessing import LabelEncoder
le = LabelEncoder()
y_enc = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(X, y_enc, test_size=0.2, random_state=42)

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

print("Train score:", model.score(X_train,y_train))
print("Test score:", model.score(X_test,y_test))

joblib.dump(model, OUT_MODEL)
joblib.dump(le, OUT_LE)
print("Saved model to", OUT_MODEL, "and label encoder to", OUT_LE)
