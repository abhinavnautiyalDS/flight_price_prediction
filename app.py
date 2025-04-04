import streamlit as st
import pickle
import pandas as pd
import numpy as np
import gdown
import base64
import os

# Only use gdown for downloading the model
file_id = "1BO-Kx_jsCYKrL9J_LQyYU0iU0wOR8frV"
output_file = "model_.pkl"

if not os.path.exists(output_file):
    gdown.download(f"https://drive.google.com/uc?id={file_id}", output_file, quiet=False)

# Install dependencies from requirements.txt (only once)
if not os.path.exists(".installed_dependencies"):
    os.system("pip install -r requirements.txt")
    open(".installed_dependencies", "w").close()

# Load background image
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("flight.jpg")  # Ensure this file exists in the directory

# Apply background styling
page_bg_img = f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{image_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Load model
with open(output_file, "rb") as f:
    model = pickle.load(f)

# Min-max scaling
def min_max_scale(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

# Min/max values used for scaling
MIN_MAX = {
    'journey_day': (1, 31),
    'journey_month': (1, 12),
    'dep_hour': (0, 23),
    'dep_min': (0, 59),
    'arrival_hour': (0, 23),
    'arrival_min': (0, 59),
    'Duration_hours': (0, 24),
    'Duration_mins': (0, 59)
}

# CSS styling for layout
st.markdown(
    """
    <style>
        .book-container {
            display: flex;
            justify-content: space-between;
            gap: 25px;
            flex-wrap: wrap;
        }
        .book-card {
            text-align: center;
            width: 18%;
            background: rgba(255, 255, 255, 0.8);
            padding: 10px;
            border-radius: 10px;
            box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
            cursor: pointer;
            border: 2px solid black;
        }
        .book-card img {
            width: 100%;
            height: auto;
            border-radius: 10px;
        }
        .book-details {
            background: rgba(0, 0, 0, 0.8);
            color: white;
            font-size: 25px;
            padding: 8px;
            border-radius: 5px;
            display: inline-block;
            margin-top: 5px;
        }
        h1 {
            font-size: 60px !important;
            font-weight: bold;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App title and input fields
st.title("✈️ Flight Price Prediction App")
st.header("Enter Flight Details:")

airline = st.selectbox("Airline", [
    'Air India', 'GoAir', 'IndiGo', 'Jet Airways',
    'Multiple carriers', 'SpiceJet', 'Vistara', 'Other'
])

source = st.selectbox("Source", ['Chennai', 'Kolkata', 'Mumbai'])
destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata'])
total_stops = st.selectbox("Total Stops", [0, 1, 2, 3])

journey_day = st.number_input
