import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Function to load data
def load_data():
    try:
        with open('appointments.json', 'r') as file:
            appointments = pd.json_normalize(json.load(file))
    except (FileNotFoundError, ValueError):
        appointments = pd.DataFrame(columns=['Date', 'Time', 'Client', 'Description'])
    return appointments

# Function to save data
def save_data(df):
    df.to_json('appointments.json', orient='records', date_format='iso', indent=4)

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
