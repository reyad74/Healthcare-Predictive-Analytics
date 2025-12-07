# app/streamlit_app.py
import streamlit as st
import requests

st.title("Patient Readmission Predictor")

age = st.number_input("Age", min_value=0, max_value=120, value=45)
bmi = st.number_input("BMI", value=25.0)
num_prior_adm = st.number_input("Prior admissions", min_value=0, value=0)

if st.button("Predict"):
    payload = {"age": age, "bmi": bmi, "num_prior_admissions": num_prior_adm}
    resp = requests.post("http://localhost:8000/predict", json=payload)
    if resp.ok:
        st.success(f"Readmission risk score: {resp.json()['readmission_score']:.3f}")
    else:
        st.error("API error")
