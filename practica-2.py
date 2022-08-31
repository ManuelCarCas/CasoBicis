from unicodedata import name
import streamlit as st
import pandas as pd
import codecs as cd
import numpy as np
#st.title('Cycles Rides in NYC')
sidebar = st.sidebar

DATE_COLUMN = 'started_at'
DATA_URL = ('citibike-tripdata.csv')

@st.cache
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    data.rename({'start_lat': 'lat', 'start_lng': 'lon'}, axis=1, inplace=True)

    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading cicle nyc data')
bike_data = load_data(1000)
data_load_state.text('Done! (using st.cache)')

if st.sidebar.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(bike_data)

if st.sidebar.checkbox('Recorridos [por hora'):
    st.subheader('Numero de recorridos por hora')

    hist_values = np.histogram(bike_data[DATE_COLUMN].dt.hour, bins=24, range=(0,24)) [0]
    st.bar_chart(hist_values)

hour_to_filter = st.sidebar.slider('hour', 0, 23, 17)
filtered_data = bike_data[bike_data[DATE_COLUMN].dt.hour == hour_to_filter]

st.subheader('Map of all pickups at %s:00' % hour_to_filter)
st.map(filtered_data)