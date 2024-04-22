import streamlit as st
import pandas as pd
import json
from datetime import datetime

# Function to load data from a JSON file
def load_data():
    try:
        with open('appointments.json', 'r') as file:
            data = json.load(file)
            appointments = pd.json_normalize(data)
    except FileNotFoundError:
        st.error("File not found. Creating a new file.")
        appointments = pd.DataFrame(columns=['Date', 'Time', 'Client', 'Description'])
    except json.JSONDecodeError:
        st.error("JSON Decode Error. Check the file's format.")
        appointments = pd.DataFrame(columns=['Date', 'Time', 'Client', 'Description'])
    return appointments

# Function to save data to a JSON file
def save_data(df):
    try:
        df.to_json('appointments.json', orient='records', date_format='iso', indent=4)
    except Exception as e:
        st.error(f"An error occurred while saving: {str(e)}")

# Streamlit application layout
st.title('Book a New Appointment')

# Load existing data
data = load_data()

# Input fields for new appointment
date = st.date_input("Date", min_value=datetime.today())
time = st.time_input("Time")
client = st.text_input("Client Name")

# Using st.text_input as a workaround for st.textarea issues
description = st.text_input("Appointment Description", max_chars=500)

# Button to add a new appointment
if st.button('Add Appointment'):
    new_data = {
        'Date': date.strftime('%Y-%m-%d'), 
        'Time': time.strftime('%H:%M'), 
        'Client': client, 
        'Description': description
    }
    data = data.append(new_data, ignore_index=True)
    save_data(data)
    st.success('Appointment added!')

# Display the table of appointments
st.write(data)
