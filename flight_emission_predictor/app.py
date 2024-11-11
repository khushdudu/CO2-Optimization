import pickle
import streamlit as st
import numpy as np
from features_lists import (
    all_features,
    aircraft_types,
    departure_airports,
    arrival_airports,
)

# Load the model
with open("./flight_emission_predictor/model/emission_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

# Streamlit app layout
st.title("Flight CO₂ Emissions Predictor")

# Form to collect user input (in main content area)
st.header("Input Parameters")
aircraft_type = st.selectbox("Aircraft Type", aircraft_types)
departure_airport = st.selectbox("Departure Airport", departure_airports)
arrival_airport = st.selectbox("Arrival Airport", arrival_airports)
distance = st.number_input("Distance (km)", min_value=0.0, step=1.0)
duration = st.number_input("Duration (hours)", min_value=0.0, step=0.1)
cruising_altitude = st.number_input("Cruising Altitude (ft)", min_value=0.0, step=100.0)
wind_speed = st.number_input("Wind Speed (km/h)", min_value=0.0, step=1.0)
temperature = st.number_input(
    "Temperature (°C)", min_value=-50.0, max_value=50.0, step=0.1
)
saf_percentage_input = st.number_input(
    "SAF Percentage (0-100%)", min_value=0.0, max_value=100.0, step=1.0
)
jet_a1_percentage_input = st.number_input(
    "Jet A-1 Percentage (0-100%)", min_value=0.0, max_value=100.0, step=1.0
)
fuel_consumption = st.number_input("Fuel Consumption (liters)", min_value=0.0, step=0.1)
passenger_load = st.number_input("Passenger Load", min_value=0, step=1)
cargo_load = st.number_input("Cargo Load (kg)", min_value=0.0, step=0.1)

# Convert SAF and Jet A-1 percentages to values that sum up to 1
# Check if the sum of SAF and Jet A-1 percentages exceeds 100
total_percentage = saf_percentage_input + jet_a1_percentage_input
if total_percentage > 100:
    saf_percentage = saf_percentage_input
    jet_a1_percentage = jet_a1_percentage_input
    st.error(
        "The sum of SAF Percentage and Jet A-1 Percentage should not exceed 100%. Please adjust your inputs."
    )
else:
    # Convert SAF and Jet A-1 percentages to values that sum up to 1
    if total_percentage > 0:
        saf_percentage = saf_percentage_input / total_percentage
        jet_a1_percentage = jet_a1_percentage_input / total_percentage
    else:
        saf_percentage = 0.0
        jet_a1_percentage = 0.0

# Prepare input feature vector
input_data = {
    "Distance (km)": distance,
    "Duration (hours)": duration,
    "Cruising Altitude (ft)": cruising_altitude,
    "Wind Speed (km/h)": wind_speed,
    "Temperature (°C)": temperature,
    "SAF Percentage": saf_percentage,
    "Jet A-1 Percentage": jet_a1_percentage,
    "Fuel Consumption (liters)": fuel_consumption,
    "Passenger Load": passenger_load,
    "Cargo Load (kg)": cargo_load,
}

# Handle one-hot encoding for categorical features
for feature in all_features:
    if feature.startswith("Aircraft Type_"):
        input_data[feature] = 1 if feature == f"Aircraft Type_{aircraft_type}" else 0
    elif feature.startswith("Departure Airport_"):
        input_data[feature] = (
            1 if feature == f"Departure Airport_{departure_airport}" else 0
        )
    elif feature.startswith("Arrival Airport_"):
        input_data[feature] = (
            1 if feature == f"Arrival Airport_{arrival_airport}" else 0
        )
    elif feature not in input_data:
        input_data[feature] = 0  # Ensure all features are present

# Convert to input array
input_features = np.array([input_data[feature] for feature in all_features]).reshape(
    1, -1
)

# Prediction button
if st.button("Predict CO₂ Emissions"):
    try:
        prediction = model.predict(input_features)
        st.success(f"Predicted CO₂ Emissions: {prediction[0]:.2f} units")
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")
