import os
import cv2
import pandas as pd
import numpy as np
from PIL import Image
import streamlit as st

from cv_module import BodyAnalyzerCV
from recommendation_engine import RecommendationEngine
from visualization import AnalyticsDashboard

# 1. Page Configuration for Smartphone Display
st.set_page_config(
    page_title="AI Wellness Analyzer",
    page_icon="🏥",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for bigger mobile touch buttons
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        height: 3em;
        font-size: 18px !important;
        font-weight: bold;
        border-radius: 10px;
    }
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📱 AI Wellness Analyzer")
st.caption("Class 11 AI Project Showcase")

# Load Engines
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")

engine = RecommendationEngine(
    os.path.join(data_dir, "food_data.csv"),
    os.path.join(data_dir, "exercise_data.csv"),
    os.path.join(data_dir, "clothing_data.csv")
)
cv_engine = BodyAnalyzerCV()

st.markdown("---")

# STEP 1: LIFESTYLE INPUTS
with st.expander("📋 **Step 1: Enter Profile & Lifestyle Habits**", expanded=True):
    name = st.text_input("Name", "Student User")
    height = st.number_input("Height (cm)", value=168.0, step=1.0)
    weight = st.number_input("Weight (kg)", value=62.0, step=0.5)
    water = st.slider("Daily Water Intake (Liters)", 0.5, 6.0, 2.0, 0.5)
    sleep = st.slider("Sleep Duration (Hours)", 3.0, 12.0, 7.0, 0.5)
    screen = st.slider("Daily Screen Time (Hours)", 1.0, 16.0, 4.0, 0.5)

# STEP 2: CAMERA / IMAGE UPLOAD
with st.expander("📸 **Step 2: Take Photo or Upload Image**", expanded=True):
    uploaded_file = st.camera_input("Take a photo using mobile camera")
    if not uploaded_file:
        uploaded_file = st.file_uploader("Or upload an image file", type=["jpg", "jpeg", "png"])

    shape_choice = "Rectangle"
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image.save("temp.jpg")
        
        with st.spinner("Analyzing silhouette..."):
            processed_img, shape, ratio = cv_engine.process_image("temp.jpg")
            
        st.image(
            cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB), 
            caption=f"Detected: {shape} (Ratio: {ratio:.2f})",
            use_container_width=True
        )
        
        shapes = ["Rectangle", "Triangle", "Inverted Triangle", "Hourglass", "Oval/Round"]
        default_idx = shapes.index(shape) if shape in shapes else 0
        shape_choice = st.selectbox("Confirm/Adjust Silhouette:", shapes, index=default_idx)

# STEP 3: RESULTS GENERATION
st.markdown("---")
if st.button("📊 Generate Mobile Wellness Report"):
    st.subheader("💡 Your AI Recommendations")
    
    bmi, category = engine.calculate_bmi(weight, height)
    st.metric(label="Calculated BMI", value=f"{bmi}", delta=category)
    st.info(f"Confirmed Silhouette: **{shape_choice}**")

    recs = engine.generate_recommendations({
        'water_intake_l': water, 
        'sleep_hours': sleep, 
        'screen_hours': screen
    })
    
    for r in recs:
        st.success(r)

    st.subheader("📈 Lifestyle Balance Chart")
    fig = AnalyticsDashboard.generate_lifestyle_chart(water, sleep, 30, screen)
    fig.set_size_inches(5, 4)
    st.pyplot(fig, use_container_width=True)
