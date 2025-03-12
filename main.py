import streamlit as st
from streamlit_option_menu import option_menu
import pickle
import warnings
import planner 
import meditate 
import pandas as pd
import plotly.express as px
from io import StringIO
import requests

# Load models
maternal_model = pickle.load(open("model/finalized_maternal_model.sav", 'rb'))
fetal_model = pickle.load(open("model/fetal_health_classifier.sav", 'rb'))

# Sidebar for navigation
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 70px;color:#DE3163;'>CareNest </h1>", unsafe_allow_html=True)
    selected = option_menu(
        menu_title='Services',
        options=['About Us', 'Pregnancy Risk Prediction', 'Fetal Health Prediction', 'Pregnancy Planner', 'Meditate'],
        icons=['info', 'heart-pulse', 'file-medical', 'pen', 'circle'],
        default_index=0
    )

# Main page content
if selected == 'About Us':
    st.title("Welcome Aboard!")
    st.subheader("Advancing Maternal and Fetal Health with Innovative Solutions")
    st.markdown("""
        At **CareNest**, we redefine maternal and fetal health management by utilizing predictive analytics to offer precise risk evaluations and actionable care plans. Our platform empowers mothers and healthcare professionals to navigate pregnancy with confidence, promoting healthier outcomes for both mother and baby.
    """)
    
    # Pregnancy Risk Prediction Section
    st.header("Pregnancy Risk Prediction")
    st.image("graphics/preg1.png", caption="Pregnancy Risk Prediction", use_container_width=True)
    st.markdown("""
        Our **Pregnancy Risk Prediction** feature utilizes advanced algorithms to assess the following parameters:
        - Age
        - Blood sugar levels
        - Blood pressure
        - Body temperature
        These insights help in managing risks during pregnancy effectively.
    """)
    
    # Fetal Health Prediction Section
    st.header("Fetal Health Prediction")
    st.image("graphics/fetus1.png", caption="Fetal Health Prediction", use_container_width=True)
    st.markdown("""
        **Fetal Health Prediction** focuses on assessing the well-being of the unborn child by analyzing:
        - Ultrasound data: Helps monitor fetal growth and detect abnormalities.
        - Maternal health: Tracks the mother's health status and its impact on the baby.
        - Genetic factors: Identifies potential genetic risks for the fetus.
    """)


if selected == 'Pregnancy Risk Prediction':
    st.title("Pregnancy Risk Prediction")
    st.markdown("""
        Pregnancy Risk Prediction involves analyzing critical parameters such as:
        - **Age**
        - **Diastolic Blood Pressure**
        - **Blood Sugar Levels**
        - **Body Temperature**
        - **Heart Rate**
    """)

    # Input for Pregnancy Risk Prediction
    age = st.text_input('Age of the Person')
    diastolicBP = st.text_input('Diastolic Blood Pressure (mmHg)')
    BS = st.text_input('Blood Sugar Levels (mmol/L)')
    bodyTemp = st.text_input('Body Temperature (°C)')
    heartRate = st.text_input('Heart Rate (bpm)')

    # Validate inputs
    if st.button('Predict Pregnancy Risk'):
        if not age or not diastolicBP or not BS or not bodyTemp or not heartRate:
            st.warning("Please fill in all fields before predicting.")
        else:
            try:
                # Check if the inputs are reasonable (positive and in a valid range)
                age = float(age)
                diastolicBP = float(diastolicBP)
                BS = float(BS)
                bodyTemp = float(bodyTemp)
                heartRate = float(heartRate)

                if age < 0 or age > 150:
                    st.warning("Please enter a valid age.")
                elif diastolicBP <= 0 or diastolicBP > 200:
                    st.warning("Please enter a valid Diastolic Blood Pressure value.")
                elif BS <= 0 or BS > 50:
                    st.warning("Please enter a valid Blood Sugar Level.")
                elif bodyTemp <= 0 or bodyTemp > 50:
                    st.warning("Please enter a valid Body Temperature.")
                elif heartRate <= 0 or heartRate > 200:
                    st.warning("Please enter a valid Heart Rate.")
                else:
                    # If all values are reasonable, predict the risk
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        predicted_risk = maternal_model.predict([[age, diastolicBP, BS, bodyTemp, heartRate]])
                        if predicted_risk[0] == 0:
                            st.success("Low Risk")
                        elif predicted_risk[0] == 1:
                            st.warning("Medium Risk")
                        else:
                            st.error("High Risk")
            except ValueError:
                st.warning("Please enter valid numeric values.")

    # Clear the inputs
    if st.button("Clear"):
        st.experimental_rerun()

if selected == 'Fetal Health Prediction':
    st.title("Fetal Health Prediction")
    st.markdown("""
        Fetal Health Prediction is essential for reducing maternal and fetal mortality rates.
        Using advanced Cardiotocograms (CTGs), we analyze critical parameters to provide actionable insights into fetal health.
    """)

    # Input for Fetal Health Prediction
    BaselineValue = st.text_input('Baseline Value')
    Accelerations = st.text_input('Accelerations')
    fetal_movement = st.text_input('Fetal Movement')
    uterine_contractions = st.text_input('Uterine Contractions')
    light_decelerations = st.text_input('Light Decelerations')
    severe_decelerations = st.text_input('Severe Decelerations')

    # Validate inputs
    if st.button('Predict Fetal Health'):
        if not BaselineValue or not Accelerations or not fetal_movement or not uterine_contractions or not light_decelerations or not severe_decelerations:
            st.warning("Please fill in all fields before predicting.")
        else:
            try:
                # Check if the inputs are reasonable (positive and in a valid range)
                BaselineValue = float(BaselineValue)
                Accelerations = float(Accelerations)
                fetal_movement = float(fetal_movement)
                uterine_contractions = float(uterine_contractions)
                light_decelerations = float(light_decelerations)
                severe_decelerations = float(severe_decelerations)

                if BaselineValue < 0 or BaselineValue > 200:
                    st.warning("Please enter a valid Baseline Value.")
                elif Accelerations < 0 or Accelerations > 200:
                    st.warning("Please enter a valid Accelerations value.")
                elif fetal_movement < 0 or fetal_movement > 200:
                    st.warning("Please enter a valid Fetal Movement value.")
                elif uterine_contractions < 0 or uterine_contractions > 200:
                    st.warning("Please enter a valid Uterine Contractions value.")
                elif light_decelerations < 0 or light_decelerations > 200:
                    st.warning("Please enter a valid Light Decelerations value.")
                elif severe_decelerations < 0 or severe_decelerations > 200:
                    st.warning("Please enter a valid Severe Decelerations value.")
                else:
                    # If all values are reasonable, predict the fetal health
                    with warnings.catch_warnings():
                        warnings.simplefilter("ignore")
                        predicted_risk = fetal_model.predict([[BaselineValue, Accelerations, fetal_movement, uterine_contractions,
                                                               light_decelerations, severe_decelerations]])
                        if predicted_risk[0] == 0:
                            st.success("Normal")
                        elif predicted_risk[0] == 1:
                            st.warning("Suspect")
                        else:
                            st.error("Pathological")
            except ValueError:
                st.warning("Please enter valid numeric values.")

    # Clear the inputs
    if st.button("Clear"):
        st.experimental_rerun()

if selected == 'Trending News':
    st.title("Trending News")
    
    # Define a list of news articles with their title, link, and image URL
    news_articles = [
        {
            'title': 'Being Told to Calm Down, Other Microaggressions May Raise Risk for Postpartum Hypertension',
            'link': 'https://www.usnews.com/news/health-news/articles/2025-01-10/being-told-to-calm-down-other-microaggressions-may-raise-risk-for-postpartum-hypertension',
            'image': 'https://www.usnews.com/object/image/00000194-5031-d463-abf5-d53167fa0000/HD1736439623186420777022.jpeg?update-time=1736510700000&size=responsiveFlow300'
        },
        {
            'title': 'Home birth service paused in Jersey',
            'link': 'https://www.bbc.com/news/articles/c4g9l224y44o',
            'image': 'https://ichef.bbci.co.uk/news/1024/cpsprodpb/946e/live/ea8b09f0-cf3d-11ef-b408-51c2ff4fda35.jpg.webp'
        },
        {
            'title': 'A Guide on What to Eat During Pregnancy',
            'link': 'https://www.healthline.com/nutrition/13-foods-to-eat-when-pregnant',
            'image': 'https://cdn.jwplayer.com/previews/27kJ06Ks'
        }
    ]
if selected == 'Pregnancy Planner':
    planner.run_planner()  

if selected == 'Meditate':
    meditate.run_meditation()  # Call the function from planner.py

