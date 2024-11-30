import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
import json

st.set_page_config(layout="wide")


geojson_url = "https://valencia.opendatasoft.com/api/v2/catalog/datasets/districtes-distritos/exports/geojson"
response = requests.get(geojson_url)

colores_distritos = {
    "EL PLA DEL REAL": "#8A2BE2",
    "EXTRAMURS": "#00CED1",
    "L'EIXAMPLE": "#FF6347",
    "ALGIROS": "#9400D3",
    "RASCANYA": "#2E8B57",
    "POBLATS DE L'OEST": "#DC143C",
    "L'OLIVERETA": "#556B2F",
    "POBLATS DEL NORD": "#00FF00",
    "BENICALAP": "#FF69B4",
    "LA SAIDIA": "#FFD700",
    "CAMINS AL GRAU": "#FF00FF",
    "BENIMACLET": "#00FFFF",
    "CAMPANAR": "#FFA500",
    "POBLATS MARITIMS": "#008080",
    "CIUTAT VELLA": "#800000",  
    "JESUS": "#FF0000", 
    "QUATRE CARRERES": "#808000", 
    "POBLATS DEL SUD": "#0000FF",
    "PATRAIX": "#D2691E" 
}

def get_color(distrito):
    return colores_distritos.get(distrito, "#D3D3D3")

def style_function(feature):
    return {
        'fillColor': get_color(feature['properties']['nombre']), 
        'color': 'black',
        'weight': 1,
        'fillOpacity': 0.5
    }

def highlight_function(feature):
    return {
        'fillColor': get_color(feature['properties']['nombre']), 
        'color': 'white',
        'weight': 2,
        'fillOpacity': 0.7
    }

if response.status_code == 200:
    geojson_data = response.json()

    col1, col2 = st.columns([1, 3])

    with col1: ## Meter más filtros
        st.header("Filtros")

        ingresos_mensuales = ["0-800", "800-1000", "1001-1500", "1501-2000", "2001-2500", "2501-3000", "+3000"]
        selected_barrios = st.multiselect("Selecciona tus ingresos mensuales brutos", ingresos_mensuales)

        alquiler = st.slider("Rango de precio de alquiler", 500, 5000, (800, 1500))
        min_alquiler, max_alquiler = alquiler

    with col2:

        m = folium.Map(location=[39.4699, -0.3763], zoom_start=12)

        tooltip = folium.features.GeoJsonTooltip(
            fields=['nombre'],
            aliases=['Distrito'],
            localize=True,
            sticky=False
        )

        folium.GeoJson(
            geojson_data,
            style_function=style_function,
            highlight_function=highlight_function,
            tooltip=tooltip
        ).add_to(m)

        folium_static(m, width=1200, height=800)

else:
    st.error("No se pudo descargar el archivo GeoJSON.")

st.markdown(
    """
    <style>
    .main {
        max-width: 100%;
        padding: 0px;
    }
    .block-container {
        padding-top: 50px;
        padding-bottom: 0px;

    }
    </style>
    """,
    unsafe_allow_html=True
)
