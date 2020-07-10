import streamlit as st
import numpy as np
import pandas as pd

st.title('Uber pickups in NYC')


DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache()
def load_data(nrows):
    data = pd.read_csv(DATA_URL , nrows = nrows)
    lowercase = lambda x :str(x).lower()
    data.rename(lowercase, axis = 'columns', inplace =True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loding data...')

data = load_data(1000)

data_load_state.text('Done! (using st.cache)')

if st.checkbox('Show Raw Data'):
    st.subheader('Raw Data')
    st.write(data)

st.subheader('Number of pickups by hour')

hist_values = np.histogram(data[DATE_COLUMN].dt.hour,
                bins = 24 , range = (0,24))[0]

st.bar_chart(hist_values)

#st.subheader('Map of all pickups')
#st.map(data)


#hour_of_filter = 10
hour_of_filter = st.slider('hour',0,23,17) # default : 17h

filtered_data = data[data[DATE_COLUMN].dt.hour == hour_of_filter] 
st.subheader(f'Map of all pickups at {hour_of_filter}:00')
st.map(filtered_data)


