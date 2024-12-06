import requests
import pandas as pd
import json

# Configuración
api_url = "https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/centros-educativos-en-valencia/records"

def fetch_and_clean_data(api_url):
    """
    Obtiene y limpia los datos de la API, conservando el nombre, código postal y coordenadas.
    """
    try:
        # Petición GET a la API
        response = requests.get(api_url)
        response.raise_for_status()  # Lanza una excepción si la petición falla
        data = response.json()  # Parsear JSON a diccionario
        
        # Filtrar los campos necesarios
        results = data.get("results", [])
        filtered_data = [
            {
                "nombre": result.get("dlibre"),
                "codigo_postal": result.get("codpos"),
                "lat": result.get("geo_point_2d", {}).get("lat"),
                "lon": result.get("geo_point_2d", {}).get("lon")
            }
            for result in results
            if result.get("dlibre")  # Validar que exista el nombre
            and result.get("codpos")  # Validar que exista el código postal
            and result.get("geo_point_2d")  # Validar que existan coordenadas
        ]
        
        # Convertir a DataFrame para manipulación adicional si es necesario
        df = pd.DataFrame(filtered_data)
        return df

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error

def save_to_json(df, output_file):
    """
    Guarda un DataFrame en formato JSON.
    - df: DataFrame con los datos.
    - output_file: Ruta del archivo JSON donde se guardarán los datos.
    """
    try:
        df.to_json(output_file, orient="records", force_ascii=False, indent=4)
        print(f"Datos guardados en {output_file}")
    except Exception as e:
        print(f"Error al guardar datos en JSON: {e}")

# Obtener y procesar los datos
data_cleaned = fetch_and_clean_data(api_url)

# Guardar los datos limpios como archivo JSON
if not data_cleaned.empty:
    output_file = "colegios_valencia.json"
    save_to_json(data_cleaned, output_file)
else:
    print("No se encontraron datos procesados.")
