import streamlit as st
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

# Function to load data from a CSV file
def load_data():
    try:
        appointments = pd.read_csv('appointments.csv')
    except FileNotFoundError:
        st.error("File not found. Creating a new file.")
        appointments = pd.DataFrame(columns=['Date', 'Time', 'Client'])
    return appointments

# Function to save data to a CSV file
def save_data(df):
    df.to_csv('appointments.csv', index=False)

# Streamlit application layout
st.title('Book a New Appointment')

# Load existing data
data = load_data()

# Input fields for new appointment
date = st.date_input("Date", min_value=datetime.today())
time = st.time_input("Time")
client = st.text_input("Client Name")

# Button to add a new appointment
if st.button('Add Appointment'):
    new_data = pd.DataFrame({'Date': [date], 'Time': [time], 'Client': [client]})
    data = pd.concat([data, new_data], ignore_index=True)
    save_data(data)
    st.success('Appointment added!')

# Display the table of appointments
st.write(data)

# Plot appointments per day of the week
if not data.empty:
    data['Date'] = pd.to_datetime(data['Date'])
    appointments_per_day = data['Date'].dt.day_name().value_counts().sort_index()
    plt.bar(appointments_per_day.index, appointments_per_day.values, color='skyblue')
    plt.xlabel('Day of the Week')
    plt.ylabel('Number of Appointments')
    plt.title('Appointments per Day of the Week')
    st.pyplot()
