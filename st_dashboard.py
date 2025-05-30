#### Import libraries ####

import streamlit as st
import pandas as pd 
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import matplotlib.pyplot as plt
from streamlit_keplergl import keplergl_static 
from keplergl import KeplerGl
from datetime import datetime as dt

#### Configure default settings ####

st.set_page_config(page_title = 'NY CitiBikes Strategy Dashboard', layout='wide')
st.markdown("This dashboard will help with uncovering insights concerning distribution logistics, availability issues, and eco-friendliness")

#### Import data #####

df = pd.read_csv('NY_plotdata.csv', index_col = 0)
top_20 = pd.read_csv('top_20.csv')

#### Define Charts ####

## Bar Chart ##

fig = go.Figure(
    go.Bar(
        x=top_20['start_station_name'],
        y=top_20['value'],
        marker=dict(
            color=top_20['value'],
            colorscale='Blues',
            colorbar=dict(title='Trips'))))

fig.update_layout(
    title='Top 20 Bike Stations in New York',
    xaxis_title='Start Stations',
    yaxis_title='Sum of Trips',
    width=900,
    height=600)

st.plotly_chart(fig, use_container_width=True)

## Line Chart ##

fig2 = make_subplots(specs = [[{"secondary_y": True}]])

fig2.add_trace(
go.Scatter(x = df['date'], y = df['rides_daily'], name = 'Daily Rides', 
marker={'color': df['rides_daily'],'color': 'blue'}),
secondary_y = False) # Primary axis

fig2.add_trace(
go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily Temperature', 
marker={'color': df['avgTemp'],'color': 'red'}),
secondary_y=True) # secondary axis

fig2.update_layout(
    title = 'Daily Trips and Temperatures in 2022',
    height = 600)

st.plotly_chart(fig2, use_container_width=True)

#### Add the map ####

html_path = "100+ Bike Trips.html"

# Read file and keep in variable 
with open(html_path, 'r') as f:
    html_data = f.read()

## Show in web page 
st.header("Aggregated Bike Trips in New York")
st.components.v1.html(html_data,height = 1000)