import streamlit as st
import numpy as np
import pickle
import base64
import os


if not os.path.exists(".installed_dependencies"):  # Run only once
    os.system("pip install -r requirements.txt")
    open(".installed_dependencies", "w").close()
# Load background image
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

image_base64 = get_base64_image("flight.jpg")

# Apply background styling
page_bg_img = f"""
<style>
.stApp {{
    background-image: url("data:image/jpg;base64,{image_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
.stButton > button {{
    display: block;
    margin: auto;
    font-size: 25px;
    padding: 10px 60px;
    border-radius: 20px;
}}
input, select {{
    font-size: 25px !important;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Load the model
with open("model_pkl1", "rb") as f:
    model = pickle.load(f)

# Scaling function
def min_max_scale(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

MIN_MAX = {
    'Day': (1, 27),
    'Month': (3, 6),
    'DURATIONHour': (0, 38),
    'Price': (1965, 52229),
}

st.markdown("<h1 style='text-align: center;'>✈️ Flight Price Predictor</h1>", unsafe_allow_html=True)

# --------- Layout: 2 columns per row ---------
col1, col2 = st.columns(2)
with col1:
    airline = st.selectbox("Airline", [
        'IndiGo', 'Air India', 'Jet Airways', 'SpiceJet',
        'Multiple carriers', 'GoAir', 'Vistara', 'Air Asia',
        'Vistara Premium economy', 'Jet Airways Business',
        'Multiple carriers Premium economy'
    ])
with col2:
    source = st.selectbox("Source", ['Banglore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai'])

col3, col4 = st.columns(2)
with col3:
    total_stops = st.selectbox("Total Stops", ['non-stop', '2 stops', '1 stop', '3 stops'])
with col4:
    destination = st.selectbox("Destination", ['New Delhi', 'Banglore', 'Cochin', 'Kolkata', 'Delhi', 'Hyderabad'])

col5, col6 = st.columns(2)
with col5:
    month = st.number_input("Journey Month", min_value=1, max_value=12, value=6)
with col6:
    day = st.number_input("Journey Day", min_value=1, max_value=31, value=15)

col7, col8 = st.columns(2)
with col7:
    dayofweek = st.selectbox("Day of Week", ['Sunday', 'Wednesday', 'Friday', 'Monday', 'Tuesday', 'Saturday', 'Thursday'])
with col8:
    daytime = st.selectbox("Time of Day", ['Night', 'Morning', 'Evening', 'Afternoon', 'Midnight'])

col9, _ = st.columns([3, 1])
with col9:
    duration_hours = st.slider("Duration (Hours)", 0, 38, 3)

# --------- Encoding & Scaling Functions ---------
def encode_inputs():
    airline_list = ['Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business',
                    'Multiple carriers', 'Multiple carriers Premium economy', 'SpiceJet',
                    'Vistara', 'Vistara Premium economy']
    source_list = ['Chennai', 'Delhi', 'Kolkata', 'Mumbai']
    destination_list = ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata', 'New Delhi']
    total_stops_list = ['2 stops', '3 stops', 'non-stop']
    dayofweek_list = ['Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday']
    daytime_list = ['Evening', 'Midnight', 'Morning', 'Night']

    encoded = []
    for item in airline_list:
        encoded.append(1 if airline == item else 0)
    for item in source_list:
        encoded.append(1 if source == item else 0)
    for item in destination_list:
        encoded.append(1 if destination == item else 0)
    for stop in total_stops_list:
        encoded.append(1 if total_stops == stop else 0)
    for day_ in dayofweek_list:
        encoded.append(1 if dayofweek == day_ else 0)
    for t in daytime_list:
        encoded.append(1 if daytime == t else 0)

    return encoded

def scale_inputs():
    inputs = {
        'Day': day,
        'Month': month,
        'DURATIONHour': duration_hours
    }
    return [min_max_scale(inputs[k], *MIN_MAX[k]) for k in inputs]

# --------- Predict Button ---------
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🎯 Predict Flight Price"):
    numerical_features = scale_inputs()
    categorical_features = encode_inputs()
    final_input = numerical_features + categorical_features
    prediction = model.predict(np.array([final_input]))[0]
    result = prediction * (52229 - 1965) + 1965
    st.success(f"💸 Predicted Flight Price: ₹{round(result, 2)}")
    st.balloons()



    
