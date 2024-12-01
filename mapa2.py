import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
import json

st.set_page_config(layout="wide")


geojson_url_1 = "https://valencia.opendatasoft.com/api/v2/catalog/datasets/districtes-distritos/exports/geojson"
response_1 = requests.get(geojson_url_1)

geojson_url_2 = "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/zonas-verdes/exports/geojson?lang=es&timezone=Europe%2FMadrid"
response_2 = requests.get(geojson_url_2)

# Estilo común para los distritos
def get_color(distrito):
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

# Estilo para las zonas verdes con rayas verdes
def green_stripes_style(feature):
    return {
        'fillColor': 'green',  # Color de fondo
        'color': 'green',  # Color del borde
        'weight': 2,  # Grosor del borde
        'fillOpacity': 0.2,  # Transparencia del relleno
        'dashArray': '5,5'  # Rayas: 5px de línea, 5px de espacio
    }

if response_1.status_code == 200 and response_2.status_code == 200:
    geojson_data_1 = response_1.json()
    geojson_data_2 = response_2.json()

    col1, col2 = st.columns([1, 3])

    with col1:
        st.header("Filtros")
        selected_ingresos = st.slider("Selecciona tus ingresos mensuales netos", 0, 10000, 3000)

    with col2:
        m = folium.Map(location=[39.4699, -0.3763], zoom_start=12)

        # Primer archivo GeoJSON: distritos
        tooltip_1 = folium.features.GeoJsonTooltip(
            fields=['nombre'],
            aliases=['Distrito'],
            localize=True,
            sticky=False
        )
        folium.GeoJson(
            geojson_data_1,
            style_function=style_function,
            highlight_function=highlight_function,
            tooltip=tooltip_1
        ).add_to(m)

        # Segundo archivo GeoJSON: zonas verdes con rayas verdes
        tooltip_2 = folium.features.GeoJsonTooltip(
            fields=['nivel3'],  # Cambiar 'nivel2' según el campo que más te interese mostrar
            aliases=['Zona Verde'],
            localize=True,
            sticky=False
        )
        folium.GeoJson(
            geojson_data_2,
            style_function=green_stripes_style,
            tooltip=tooltip_2
        ).add_to(m)

        folium_static(m, width=1200, height=800)

else:
    st.error("No se pudieron descargar los archivos GeoJSON.")

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
