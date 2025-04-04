import streamlit as st
import numpy as np
import pickle
import base64
import gdown
import sklearn

pip install --no-cache-dir scikit-learn


if not os.path.exists(".installed_dependencies"):  # Run only once
    os.system("pip install -r requirements.txt")
    open(".installed_dependencies", "w").close()

# Google Drive file ID
file_id = "1BO-Kx_jsCYKrL9J_LQyYU0iU0wOR8frV"
output_file = "model_.pkl"

gdown.download(f"https://drive.google.com/uc?id={file_id}", output_file, quiet=False)
# Load trained model
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Replace with your local image file path (ensure it's in the same directory or provide full path)
image_base64 = get_base64_image("flight.jpg")  # Change "background.jpg" to your image filename

# CSS for setting background image
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
with open(output_file, "rb") as f:
    model = pickle.load(f)

# Scaling function
def min_max_scale(value, min_val, max_val):
    return (value - min_val) / (max_val - min_val)

# Min/max values from training data
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
            border: 2px solid black; /* Black border around book cards */
        }

        .book-card img {
            width: 100%;
            height: auto;
            border-radius: 10px;
        }

        .book-details {
            background: rgba(0, 0, 0, 0.8); /* Black background for better readability */
            color: white;
            font-size: 25px; /* Increase font size */
            padding: 8px;
            border-radius: 5px;
            display: inline-block;
            margin-top: 5px;
        }

        h1 {
            font-size: 60px !important; /* Increase title size */
            font-weight: bold;
            text-align: center;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


st.title("✈️ Flight Price Prediction App")

# User Inputs
st.header("Enter Flight Details:")

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

# One-hot encoding (manual)
def encode_inputs():
    airline_list = ['Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Multiple carriers', 'Other', 'SpiceJet', 'Vistara']
    source_list = ['Chennai', 'Kolkata', 'Mumbai']
    destination_list = ['Cochin', 'Delhi', 'Hyderabad', 'Kolkata']

    airline_encoded = [1 if airline == name else 0 for name in airline_list]
    source_encoded = [1 if source == src else 0 for src in source_list]
    dest_encoded = [1 if destination == dest else 0 for dest in destination_list]

    return airline_encoded + source_encoded + dest_encoded

# Scale numerical inputs
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

# Predict button
if st.button("Predict Flight Price"):
    numerical_features = scale_inputs()
    categorical_features = encode_inputs()
    final_input = [total_stops] + numerical_features + categorical_features

    prediction = model.predict(np.array([final_input]))[0]
    st.success(f"Predicted Flight Price: ₹{round(prediction, 2)}")
