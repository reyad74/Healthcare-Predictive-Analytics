# app/streamlit_app.py
import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Healthcare Readmission Predictor",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Sidebar Navigation
with st.sidebar:
    st.title("📋 Menu")
    page = st.radio("Select Section", ["🏥 Home", "📊 Dashboard", "ℹ️ About"])

# Main Header
st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #0066cc; margin-bottom: 5px;">🏥 Healthcare Readmission Predictor</h1>
        <p style="color: #666; font-size: 18px;">AI-Powered Risk Assessment Tool</p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

if page == "🏥 Home":
    st.markdown("## 👤 Patient Risk Assessment")
    
    # Input Section
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Patient Information")
        age = st.slider("Age (years)", min_value=0, max_value=120, value=45, help="Patient's age in years")
        bmi = st.number_input("Body Mass Index (BMI)", min_value=10.0, max_value=60.0, value=25.0, step=0.1, help="BMI value")
    
    with col2:
        st.markdown("### 📊 Medical History")
        num_prior_adm = st.number_input("Number of Prior Admissions", min_value=0, max_value=20, value=0, step=1, help="Total number of previous hospital admissions")
    
    st.markdown("---")
    
    # Prediction button
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        predict_button = st.button("🔮 Predict Readmission Risk", use_container_width=True, key="predict")
    
    # Show prediction results
    if predict_button:
        with st.spinner("🔄 Analyzing patient data..."):
            try:
                payload = {
                    "age": float(age),
                    "bmi": float(bmi),
                    "num_prior_admissions": int(num_prior_adm)
                }
                resp = requests.post("http://localhost:8000/predict", json=payload, timeout=10)
                
                if resp.ok:
                    result = resp.json()
                    score = result['readmission_score']
                    
                    # Determine risk level
                    if score >= 0.7:
                        risk_level = "🔴 HIGH RISK"
                        risk_color = "#ef476f"
                        recommendation = "Immediate intervention recommended"
                    elif score >= 0.4:
                        risk_level = "🟡 MEDIUM RISK"
                        risk_color = "#ffd166"
                        recommendation = "Monitor closely and provide support"
                    else:
                        risk_level = "🟢 LOW RISK"
                        risk_color = "#06d6a0"
                        recommendation = "Standard care protocol"
                    
                    # Display results
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 📊 Prediction Results")
                    
                    result_col1, result_col2 = st.columns(2)
                    
                    with result_col1:
                        st.markdown(f"""
                            <div style="background-color: {risk_color}; color: white; padding: 20px; border-radius: 10px; text-align: center;">
                                <h2 style="margin: 0 0 10px 0;">{risk_level}</h2>
                                <h1 style="margin: 0 0 10px 0; font-size: 3em;">{score:.1%}</h1>
                                <p style="margin: 0;">{recommendation}</p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown("### 📋 Patient Summary")
                        st.info(f"""
                            **Age:** {age} years
                            
                            **BMI:** {bmi:.1f}
                            
                            **Prior Admissions:** {num_prior_adm}
                            
                            **Assessment Time:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
                        """)
                    
                    with result_col2:
                        # Risk gauge chart
                        fig = go.Figure(go.Indicator(
                            mode="gauge+number",
                            value=score * 100,
                            domain={'x': [0, 1], 'y': [0, 1]},
                            title={'text': "Risk Score (%)"},
                            gauge={
                                'axis': {'range': [0, 100]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 40], 'color': "#06d6a0"},
                                    {'range': [40, 70], 'color': "#ffd166"},
                                    {'range': [70, 100], 'color': "#ef476f"}
                                ],
                                'threshold': {
                                    'line': {'color': "red", 'width': 4},
                                    'thickness': 0.75,
                                    'value': 75
                                }
                            }
                        ))
                        fig.update_layout(height=400, margin=dict(l=20, r=20, t=80, b=20))
                        st.plotly_chart(fig, use_container_width=True)
                    
                    # Recommendations box
                    st.markdown("<br>", unsafe_allow_html=True)
                    st.markdown("### 💡 Clinical Recommendations")
                    
                    if score >= 0.7:
                        st.error("""
                            **🔴 High Risk Patient - Immediate Action Required**
                            
                            • Schedule immediate follow-up appointments
                            • Consider intensive care management
                            • Provide comprehensive discharge planning
                            • Arrange home health services if needed
                        """)
                    elif score >= 0.4:
                        st.warning("""
                            **🟡 Medium Risk Patient - Careful Monitoring**
                            
                            • Schedule timely follow-up visits
                            • Ensure medication adherence
                            • Provide patient education materials
                            • Monitor vital signs regularly
                        """)
                    else:
                        st.success("""
                            **🟢 Low Risk Patient - Standard Care**
                            
                            • Standard post-discharge care
                            • Routine follow-up as needed
                            • Patient to call if concerns arise
                        """)
                else:
                    st.error(f"❌ API Error: {resp.status_code}")
            
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to prediction API. Make sure the FastAPI server is running on http://localhost:8000")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

elif page == "📊 Dashboard":
    st.markdown("## 📈 Analytics Dashboard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Predictions", "0", "0 today")
    
    with col2:
        st.metric("High Risk Cases", "0", "0 today")
    
    with col3:
        st.metric("Medium Risk Cases", "0", "0 today")
    
    with col4:
        st.metric("Low Risk Cases", "0", "0 today")
    
    st.markdown("---")
    st.info("📈 Dashboard data will be populated as predictions are made.")

elif page == "ℹ️ About":
    st.markdown("## ℹ️ About This Application")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🎯 Purpose")
        st.markdown("""
        The Healthcare Readmission Predictor is an AI-powered risk assessment tool designed to identify patients 
        at high risk of hospital readmission within 30 days of discharge.
        """)
        
        st.markdown("### 🔬 Technology Stack")
        st.markdown("""
        - **ML Models**: XGBoost & Random Forest
        - **Backend**: FastAPI
        - **Frontend**: Streamlit
        - **Data Processing**: Pandas, Scikit-learn, NumPy
        """)
    
    with col2:
        st.markdown("### 📊 Model Features")
        st.markdown("""
        The prediction model considers:
        - Patient age
        - Body Mass Index (BMI)
        - Number of prior hospital admissions
        """)
        
        st.markdown("### 📞 Support")
        st.markdown("""
        For issues or questions, please contact the development team.
        """)
    
    st.markdown("---")
    st.warning("""
        ⚠️ **Important Disclaimer**
        
        This tool is for clinical decision support only and should not replace professional medical judgment.
        Always consult with healthcare professionals for definitive diagnoses and treatment plans.
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style='text-align: center; color: #666; font-size: 12px; margin-top: 20px;'>
        <p>Healthcare Readmission Predictor © 2025 | Powered by AI</p>
        <p>⚕️ For clinical decision support only</p>
    </div>
""", unsafe_allow_html=True)
