import pandas as pd
import numpy as np
from streamlit_folium import st_folium
import streamlit as st
import folium
import geocoder
import requests
from streamlit_lottie import st_lottie

data = "https://github.com/Ck991234/foxy/blob/f29a9bfea28ca68a776687946d914c3319517f23/zomatogeo.csv?raw=true"
lottie_url = "https://assets2.lottiefiles.com/packages/lf20_mksle47o.json"


def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_json = load_lottieurl(lottie_url)
st_lottie(lottie_json)

st.sidebar.title('Pune Hotel Recommendation Engine')

location = st.sidebar.text_input('Type Any Pune Location, It Will Show You 10 Closest Hotels Near You')


# Geo Location Extractor

def get_geolocation(place):
    g = geocoder.arcgis(str(place) + "," + "Pune")
    return g.latlng


latlog = get_geolocation(location)
st.write('Your Geo Location Is ', latlog[0], latlog[1])


# KNN Algorithm
@st.cache_data
def topt(lattitude, longitude):
    df = pd.read_csv(data, index_col=0)
    inlattitude = lattitude * np.pi / 180
    inlongitude = longitude * np.pi / 180
    df["e_distance"] = np.sqrt(((inlattitude - df["rad_latit"]) ** 2) + ((inlongitude - df["rad_longi"]) ** 2))
    df2 = {'Restaurant_Name': 'My Current Location', 'longitude': longitude, 'lattitude': lattitude, 'e_distance': 0}
    df1 = pd.concat([df, df2], ignore_index=True)
    final_data = df1.sort_values(["e_distance"], ascending=True).head(10)
    final_data.rename(columns={'longitude': 'long', 'lattitude': 'lat'}, inplace=True)
    return final_data


top_20 = topt(latlog[0], latlog[1])
st.sidebar.write(top_20["Restaurant_Name"])

# Center on Liberty Bell, add marker
m = folium.Map(location=[latlog[0], latlog[1]], zoom_start=16)
folium.Marker(
    [latlog[0], latlog[1]],
    popup="Your Location",
    tooltip="Your Location"
).add_to(m)

for i in range(0, len(top_20)):
    folium.Marker([top_20.iloc[i]["lat"], top_20.iloc[i]["long"]], popup=top_20.iloc[i]["Restaurant_Name"],
                  tooltip=top_20.iloc[i]["Restaurant_Name"]).add_to(m)

# Call to render Folium map in Streamlit
st_data = st_folium(m, width=600)
st.write(st_data)  # Add this line to display the map

