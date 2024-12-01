import streamlit as st
import folium
from streamlit_folium import folium_static
import requests
import json
from pymongo import MongoClient

client = MongoClient('mongodb://root:example@mongo:27017')
db = client['DATA_PROY_1']
collection = db['precio_alq_m2']
documentos = collection.find()

st.set_page_config(layout="wide")

geojson_url_1 = "https://valencia.opendatasoft.com/api/v2/catalog/datasets/districtes-distritos/exports/geojson"
response_1 = requests.get(geojson_url_1)

geojson_url_2 = "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/zonas-verdes/exports/geojson?lang=es&timezone=Europe%2FMadrid"
response_2 = requests.get(geojson_url_2)

def get_color(distrito):
    colores_distritos = {
        "EL PLA DEL REAL": "##FF0000",
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
        "JESUS": "8A2BE2", 
        "QUATRE CARRERES": "#808000", 
        "POBLATS DEL SUD": "#0000FF",
        "PATRAIX": "#D2691E" 
    }
    if distrito in distritos_aptos:
        return colores_distritos.get(distrito, "#D3D3D3")
    return "#D3D3D3"


def style_function(feature, context=None):
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

def green_stripes_style(feature):
    return {
        'fillColor': 'green',
        'color': 'green',
        'weight': 2, 
        'fillOpacity': 0.2,
        'dashArray': '5,5'
    }

def filtrar_ingresos(precio_2022_m2, ingreso_maximo, area_promedio=60):
    alquiler_mensual = float(precio_2022_m2) * area_promedio
    return alquiler_mensual <= 0.4 * ingreso_maximo

def obtener_distritos_aptos(ingreso_maximo, area_promedio=90):
    distritos_aptos = []
    for documento in documentos:
        distrito = documento['distrito']
        precio_2022_m2 = float(documento['precio_2022_m2'])
        
        if filtrar_ingresos(precio_2022_m2, ingreso_maximo, area_promedio):
            distritos_aptos.append(distrito)
    return distritos_aptos


if response_1.status_code == 200 and response_2.status_code == 200:
    geojson_data_1 = response_1.json()
    geojson_data_2 = response_2.json()

    col1, col2 = st.columns([1, 3])

    with col1:
        st.header("Filtros")
        selected_ingresos = st.slider("Selecciona tus ingresos mensuales netos", 0, 10000, 3000)

        st.header("Control de capas")
        show_districts = st.checkbox("Mostrar Distritos", value=True)
        show_green_zones = st.checkbox("Mostrar Zonas Verdes", value=True)
        
    with col2:
        distritos_aptos = obtener_distritos_aptos(selected_ingresos)
        m = folium.Map(location=[39.4699, -0.3763], zoom_start=12)

        district_group = folium.FeatureGroup(name="Distritos")
        green_zone_group = folium.FeatureGroup(name="Zonas Verdes")

        # Primer archivo GeoJSON: distritos
        tooltip_1 = folium.features.GeoJsonTooltip(
            fields=['nombre'],
            aliases=['Distrito'],
            localize=True,
            sticky=False
        )
        folium.GeoJson(
            geojson_data_1,
            style_function=lambda feature: style_function(feature, distritos_aptos),
            highlight_function=highlight_function,
            tooltip=tooltip_1
        ).add_to(district_group)

        # Segundo archivo GeoJSON: zonas verdes con rayas verdes
        tooltip_2 = folium.features.GeoJsonTooltip(
            fields=['nivel3'],
            aliases=['Zona Verde'],
            localize=True,
            sticky=False
        )
        folium.GeoJson(
            geojson_data_2,
            style_function=green_stripes_style,
            tooltip=tooltip_2
        ).add_to(green_zone_group)

        if show_districts:
            district_group.add_to(m)
        if show_green_zones:
            green_zone_group.add_to(m)



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
