import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="Energy Dashboard", layout="wide")
st.title("⚡ Interactive Energy Market Dashboard")
st.write("Live Onshore Wind Generation Data from SMARD")

# Connect to the database and cache the results for performance


@st.cache_data
def load_data():
    conn = sqlite3.connect("energy_data.db")
    # Load data and parse the timestamps correctly
    df = pd.read_sql_query("SELECT * FROM wind_onshore",
                           conn, parse_dates=["Datetime"])
    conn.close()
    return df


# Fetch data
df = load_data()

# Display the raw data table
st.dataframe(df.head(10))

# --- Visualizations ---
st.subheader("Wind Generation Over Time")

# Create an interactive line chart using Plotly
fig = px.line(
    df,
    x="Datetime",
    y="Megawatts",
    title="Onshore Wind Power Generation",
    labels={"Datetime": "Time", "Megawatts": "Generation (MW)"}
)

# Customizing the chart appearance
fig.update_layout(
    xaxis_title="Date & Time",
    yaxis_title="Megawatts (MW)",
    template="plotly_dark"
)

# Render the chart in Streamlit
st.plotly_chart(fig, width="stretch")
