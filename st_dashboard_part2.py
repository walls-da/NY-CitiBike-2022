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
from PIL import Image
from numerize.numerize import numerize

#### Configure default settings ####

st.set_page_config(page_title = 'NY CitiBikes Strategy Dashboard', layout='wide')

## Define side bar ## 
st.sidebar.title("Topic Selector")
page = st.sidebar.selectbox('Select an analysis topic',
   ["Intro Page",  "Weather and Bike Usage", "Top 20 Stations", "Interactive Map and Bike Trips", "Recommendations"])

#### Import data #####

df = pd.read_csv('reduced_data_to_plot.csv', index_col = 0)
top_20 = pd.read_csv('top_20.csv')

#### Define Pages ####

## Intro Page ##

if page == "Intro Page":
    st.markdown("#### This dashboard will help with uncovering insights concerning distribution logistics, availability issues, and eco-friendliness.")
    st.markdown("Since COVID-19, there has been a higher demand for NY CitiBike bikes. This has resulted in customer frustration because bikes cannot always be rented out or turned in. This analysis will look at the potential reasons behind this. The dashboard is separated into 4 sections:")
    st.markdown("- Top 20 Stations")
    st.markdown("- Weather and Bike Usage")
    st.markdown(" - Interactive Map and Bike Trips")
    st.markdown(" - Recommendations")
    st.markdown(" - The dropdown menu on the left, 'Aspect Selector', will take you to the different aspects of the analysis.")

    myImage = Image.open("set-bikes-outdoors.jpg") #source Unsplash
    st.image(myImage)

    ## Dual Axis Line Chart ##

elif page == 'Weather and Bike Usage':

    ## Line chart ##
    fig2 = make_subplots(specs = [[{"secondary_y": True}]])

    fig2.add_trace(
    go.Scatter(x = df['date'], y = df['rides_daily'], name = 'Daily Rides', 
    marker={'color':df['rides_daily'],'color': 'blue'}),
    secondary_y = False) # Primary axis
    
    fig2.add_trace(
    go.Scatter(x=df['date'], y = df['avgTemp'], name = 'Daily Temperature', 
    marker={'color': df['avgTemp'],'color': 'red'}),
    secondary_y=True) # secondary axis
    
    fig2.update_layout(
        title = 'Daily Trips and Temperatures in 2022',
        height = 600)
    
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("This chart illustrates the correlation bike usage and temperature has as both lines rise and fall together. Regardless of season, the warmer the temperature, the more bike trips there are. Additionally, the warmer months have the highest bike usage and trips. These summer months could be where we see an increase in user frustration")

#### Top 20 Stations ####

elif page == 'Top 20 Stations':

    ## Sort data by season ##
    with st.sidebar:
             season_filter = st.multiselect(label= 'Select Season', options=df['season'].unique(),
         default=df['season'].unique())
    
    df_season = df.query('season == @season_filter')

    ## Define Total Rides ##
    total_rides = float(df_season['rides_daily'].count())    
    st.metric(label = 'Total Bike Rides', value= numerize(total_rides))
        
    ## Bar Chart ##

    df_season['value'] = 1
    df_groupby_bar = df_season.groupby('start_station_name', as_index = False).agg({'value': 'sum'}) 
    top_20 = df_groupby_bar.nlargest(20, 'value')

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
    st.markdown("Though these are the top stations, the most popular station has 4,237 trips and the lowest has 2,823. With the lowest top station having almost just half the trips as the most used station, it is clearly illustrated there are definite preferences. Using the interactive map (which you can access with the selector) can be used to determine why some stations are seeing double the amount of usage")


#### Interactive map and Bike Trips ####

elif page == 'Interactive Map and Bike Trips':

    ## Add the Map ##
    html_path = "100+ Bike Trips.html"

    # Read file and keep in variable 
    with open(html_path, 'r') as f:
        html_data = f.read()

    ## Show in web page 
    st.header("Aggregated Bike Trips in New York")
    st.components.v1.html(html_data,height = 1000)
    st.markdown("After filtering the map, we can see that, although 21st & 6 Ave is the top start station, it only has 1 trip that also ends at the same station. It can be gathered that most customers dock their bikes at a different station despite starting at 21st & 6 ave.")
    st.markdown("There are 6 stations that do not have an end station:")
    st.markdown("12 Ave & W 40 St, 5 Ave & E 72 St, Roosevelt Island Tramway,Grand Army Plaza, 6 Ave & Central Park S, and 7 Ave & Central Park S")
    st.markdown("Likely customers are running into the issue of not having enough space to dock their bikes for return after leaving these stations.")

else: 
    st.header("Conclusion and Recommendations") 
    bikes = Image.open("rec.jpg") #source: Unsplash
    st.image(bikes)

    st.markdown("From the analysis, CitiBike should focus on the following:")
    st.markdown("- Consider adding other stations around 12 Ave & W 40 St, 5 Ave & E 72 St, Roosevelt Island Tramway,Grand Army Plaza, 6 Ave & Central Park S, and 7 Ave & Central Park S as these stations often experience no returns") 
    st.markdown("- During the summer, make sure populat stations are well stocked. This especially includes: W 21st & 6 Ave, West St & Chamber St, Broadway & W 58 St")
    st.markdown(" - Winter and cooler months can have a reduced number of bikes supplied as usage decreases")