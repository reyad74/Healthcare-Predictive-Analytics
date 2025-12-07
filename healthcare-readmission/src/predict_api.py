# src/predict_api.py
from fastapi import FastAPI, HTTPException
import joblib
import pandas as pd
from pydantic import BaseModel
import os

app = FastAPI()

# load models and transformers
rf = None
xgb = None
imputer = None
scaler = None

def load_models():
    global rf, xgb, imputer, scaler
    try:
        rf = joblib.load('models/rf.joblib')
        xgb = joblib.load('models/xgb.joblib')
        imputer = joblib.load('models/imputer.joblib')
        scaler = joblib.load('models/scaler.joblib')
    except FileNotFoundError as e:
        print(f"Warning: Could not load models - {e}")
        print("Please run src/train.py first to generate the models")

load_models()

class Patient(BaseModel):
    # put example features; change according to your dataset
    age: float
    bmi: float
    num_prior_admissions: int
    # add more features...

@app.post("/predict")
def predict(p: Patient):
    if rf is None or xgb is None or imputer is None or scaler is None:
        raise HTTPException(status_code=503, detail="Models not loaded. Please run src/train.py first to generate the models.")
    
    data = pd.DataFrame([p.dict()])
    data_imputed = pd.DataFrame(imputer.transform(data), columns=data.columns)
    data_scaled = pd.DataFrame(scaler.transform(data_imputed), columns=data.columns)
    rf_pred = rf.predict_proba(data_scaled)[:,1][0]
    xgb_pred = xgb.predict_proba(data_scaled)[:,1][0]
    # ensemble (simple average)
    score = (rf_pred + xgb_pred) / 2.0
    return {"readmission_score": float(score)}
