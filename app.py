import streamlit as st
import pandas as pd
import json

# Load the data from the JSON file
with open('extracted_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)['data']

# Convert the data to a pandas DataFrame
df = pd.DataFrame(data)

# Convert "Výměra [m2]:" column to numeric for sorting and filtering
df["Výměra [m2]:"] = pd.to_numeric(df["Výměra [m2]:"], errors='coerce')

# Sidebar filters
st.sidebar.header("Filters")

# Filter by "Druh pozemku:"
druh_pozemku_values = df["Druh pozemku:"].unique()
selected_druh_pozemku = st.sidebar.multiselect("Select Druh pozemku", druh_pozemku_values, default=druh_pozemku_values)

# Filter the dataframe based on selected "Druh pozemku:"
df_filtered = df[df["Druh pozemku:"].isin(selected_druh_pozemku)]

# Select range for "Výměra [m2]:" using slider
min_vymera, max_vymera = int(df["Výměra [m2]:"].min()), int(df["Výměra [m2]:"].max())
selected_vymera_slider = st.sidebar.slider("Select range of Výměra [m2]: (Slider)", min_vymera, max_vymera, (min_vymera, max_vymera))

# Select range for "Výměra [m2]:" using input boxes
st.sidebar.markdown("### Select range of Výměra [m2]: (Input Boxes)")
selected_vymera_min = st.sidebar.number_input("Min Výměra [m2]:", min_value=min_vymera, max_value=max_vymera, value=min_vymera)
selected_vymera_max = st.sidebar.number_input("Max Výměra [m2]:", min_value=min_vymera, max_value=max_vymera, value=max_vymera)

# Ensure input box values are in correct order
if selected_vymera_min > selected_vymera_max:
    st.sidebar.error("Min Výměra [m2]: should be less than or equal to Max Výměra [m2]:")

# Choose which range to use (if both inputs are changed, priority is given to the last changed input)
selected_vymera = (selected_vymera_min, selected_vymera_max)

# Filter dataframe based on selected range of "Výměra [m2]:"
df_filtered = df_filtered[(df_filtered["Výměra [m2]:"] >= selected_vymera[0]) & (df_filtered["Výměra [m2]:"] <= selected_vymera[1])]

# Sort by "Výměra [m2]:"
sort_order = st.sidebar.radio("Sort by Výměra [m2]:", ("Ascending", "Descending"))
df_filtered = df_filtered.sort_values(by="Výměra [m2]:", ascending=(sort_order == "Ascending"))

# Main area
st.title("Parcel Data Viewer")
st.write("This app allows you to view, filter, and sort parcel data.")

# Display the filtered and sorted data
st.dataframe(df_filtered)

# Show the statistics
st.header("Statistics")
st.write(f"Total Parcels: {df_filtered.shape[0]}")
st.write(f"Total Area: {df_filtered['Výměra [m2]:'].sum()} m²")
