import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Function to load data
def load_data():
    try:
        with open('appointments.json', 'r') as file:
            data = json.load(file)
            appointments = pd.json_normalize(data)
            st.write("Loaded data successfully!")  # Debug message
    except FileNotFoundError:
        st.error("File not found. Creating a new file.")
        appointments = pd.DataFrame(columns=['Date', 'Time', 'Client', 'Description'])
    except json.JSONDecodeError:
        st.error("JSON Decode Error. Check the file's format.")
        appointments = pd.DataFrame(columns=['Date', 'Time', 'Client', 'Description'])
    return appointments

# Function to save data
def save_data(df):
    try:
        df.to_json('appointments.json', orient='records', date_format='iso', indent=4)
        st.write("Data saved successfully!")  # Debug message
    except Exception as e:
        st.error(f"An error occurred while saving: {str(e)}")

# Title of the app
st.title('Book a New Appointment')

# Load existing data
data = load_data()

# Input fields for new appointment
date = st.date_input("Date", min_value=datetime.today())
time = st.time_input("Time")
client = st.text_input("Client Name")
description = st.textarea("Appointment Description")

# Button to add a new appointment
if st.button('Add Appointment'):
    new_data = {'Date': date.strftime('%Y-%m-%d'), 'Time': time.strftime('%H:%M'), 'Client': client, 'Description': description}
    data = data.append(new_data, ignore_index=True)
    save_data(data)
    st.success('Appointment added!')

# Show table of appointments
st.write(data)
