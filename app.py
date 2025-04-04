import streamlit as st
import pickle
import pandas as pd
import numpy as np
import base64
import os
import requests

# --- Google Drive model download (replacing gdown) ---
def download_file_from_google_drive(file_id, destination):
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    session = requests.Session()

    response = session.get(url, stream=True)
    token = get_confirm_token(response)

    if token:
        params = {"confirm": token}
        response = session.get(url, params=params, stream=True)

    save_response_content(response, destination)

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith("download_warning"):
            return value
    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768
    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk:
                f.write(chunk)

# Download model if not already present
model_file = "model_.pkl"
if not os.path.exists(model_file):
    file_id = "1BO-Kx_jsCYKrL9J_LQyYU0iU0wOR8frV"  # Google Drive file ID
    download_file_from_google_drive(file_id, model_file)

# Load model
with open(model_file, "rb") as f:
    model = pickle.load(f)

# --- Background image ---
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("flight.jpg")

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

# --- CSS for layout and title ---
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
        h1 {{
            font-size: 60px !important;
            font-weight: bold;
            text-align: center;
        }}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("✈️ Flight Price Prediction App")
st.header("Enter Flight Details:")

# --- Input collection ---
airline = st.selectbox("Airline", [
    'Air India', 'GoAir', 'IndiGo', 'Jet Airways',
    'Multiple carriers', 'SpiceJet', 'Vistara', 'Other'
])
source = st.selectbox("Source", ['Chennai', 'Kolkata', 'Mumbai'])
destination = st.selectbox("Destination", ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata'])
total_stops = st.selectbox("Total Stops", [0, 1, 2, 3])

journey_day = st.number_input("Journey Day", min_value=1, max_value=31, value=15)
journey_month = st.number_input("Journey Month", min_value=1, max_value=12, value=6)

dep_hour = st.slider("Departure Hour", 0, 23, 12)
dep_min = st.slider("Departure Minute", 0, 59, 30)
arrival_hour = st.slider("Arrival Hour", 0, 23, 15)
arrival_min = st.slider("Arrival Minute", 0, 59, 50)
duration_hours = st.slider("Duration Hours", 0, 24, 3)
duration_mins = st.slider("Duration Minutes", 0, 59, 20)

# --- Manual encoding ---
def encode_inputs():
    airline_list = ['Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Multiple carriers', 'Other', 'SpiceJet', 'Vistara']
    source_list = ['Chennai', 'Kolkata', 'Mumbai']
    destination_list = ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata']
    airline_encoded = [1 if airline == name else 0 for name in airline_list]
    source_encoded = [1 if source == src else 0 for src in source_list]
    dest_encoded = [1 if destination == dest else 0 for dest in destination_list]
    return airline_encoded + source_encoded + dest_encoded

# --- Scaling numerical features ---
def min_max_scale(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

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

def scale_inputs():
    inputs = {
        'journey_day': journey_day,
        'journey_month': journey_month,
        'dep_hour': dep_hour,
        'dep_min': dep_min,
        'arrival_hour': arrival_hour,
        'arrival_min': arrival_min,
        'Duration_hours': duration_hours,
        'Duration_mins': duration_mins
    }
    return [min_max_scale(inputs[k], *MIN_MAX[k]) for k in inputs]

# --- Prediction ---
if st.button("Predict Flight Price"):
    numerical_features = scale_inputs()
    categorical_features = encode_inputs()
    final_input = [total_stops] + numerical_features + categorical_features
    prediction = model.predict(np.array([final_input]))[0]
    st.success(f"Predicted Flight Price: ₹{round(prediction, 2)}")
