import streamlit as st
import geopandas as gpd
import json
import zipfile
import os
import folium
from folium import GeoJson

# Función para extraer y convertir Shapefile a GeoJSON
def shp_to_geojson(zip_path, shp_name, shx_name, dbf_name):
    with zipfile.ZipFile(zip_path, 'r') as z:
        z.extractall("shapefile")
    
    shp_path = os.path.join("shapefile", shp_name)
    shx_path = os.path.join("shapefile", shx_name)
    dbf_path = os.path.join("shapefile", dbf_name)
    
    if not os.path.exists(shp_path) or not os.path.exists(shx_path) or not os.path.exists(dbf_path):
        st.error("Los archivos .shp, .shx, o .dbf no se encontraron en el ZIP.")
        return None
    
    try:
        gdf = gpd.read_file(shp_path)
        geojson = gdf.to_json()
    except Exception as e:
        st.error(f"Error al leer el archivo Shapefile: {e}")
        return None

    return geojson

def show_map(geojson_data):
    m = folium.Map(location=[39.4699, -0.3763], zoom_start=12)
    
    GeoJson(geojson_data).add_to(m)

    map_html_path = "map.html"
    m.save(map_html_path)

    return map_html_path

uploaded_file = st.file_uploader("Elige un archivo Shapefile (ZIP)", type="zip")

if uploaded_file is not None:
    zip_path = "uploaded_shapefile.zip"
    with open(zip_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    shp_name = "ALQ_Municipios_2022_Web.shp"
    shx_name = "ALQ_Municipios_2022_Web.shx"
    dbf_name = "ALQ_Municipios_2022_Web.dbf"

    geojson_data = shp_to_geojson(zip_path, shp_name, shx_name, dbf_name)

    if geojson_data:
        st.write("GeoJSON:")
        st.json(json.loads(geojson_data))

        map_html_path = show_map(json.loads(geojson_data))

        st.markdown(f'<iframe src="file://{map_html_path}" width="700" height="500"></iframe>', unsafe_allow_html=True)

    for filename in os.listdir("shapefile"):
        file_path = os.path.join("shapefile", filename)
        os.remove(file_path)
    os.rmdir("shapefile")
    os.remove(zip_path)
    