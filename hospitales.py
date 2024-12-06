import requests
from collections import defaultdict
import json

def obtener_todos_hospitales(url):
    """
    Obtiene TODOS los registros de hospitales desde la API de Valencia.
    """
    hospitales_total = []
    
    try:
        parametros = {
            'limit': 100,
            'offset': 0
        }
        
        while True:
            respuesta = requests.get(url, params=parametros)
            respuesta.raise_for_status()
            
            datos = respuesta.json()
            
            hospitales_parcial = [
                {
                    'nombre': hospital['nombre'], 
                    'distrito': hospital['coddistrit'],
                    'financiacion': hospital.get('financiaci', 'No especificado')
                } 
                for hospital in datos['results'] 
                if hospital.get('tipo') == 'Hospital'
            ]
            
            hospitales_total.extend(hospitales_parcial)
            
            if len(datos['results']) < parametros['limit']:
                break
            
            parametros['offset'] += parametros['limit']
        
        return hospitales_total
    
    except requests.RequestException as e:
        print(f"Error al obtener datos de la API: {e}")
        return []

def agrupar_hospitales_por_distrito(hospitales):
    """
    Agrupa los hospitales por distrito en formato JSON.
    """
    distritos = defaultdict(lambda: {
        'total_hospitales': 0,
        'nombres_hospitales': [],
        'tipos_financiacion': {}
    })
    
    for hospital in hospitales:
        distrito = hospital['distrito']
        
        distritos[distrito]['total_hospitales'] += 1
        distritos[distrito]['nombres_hospitales'].append(hospital['nombre'])
        
        financiacion = hospital['financiacion']
        if financiacion not in distritos[distrito]['tipos_financiacion']:
            distritos[distrito]['tipos_financiacion'][financiacion] = 0
        distritos[distrito]['tipos_financiacion'][financiacion] += 1
    
    return dict(distritos)

# URL del endpoint de la API de Valencia
url_api = 'https://valencia.opendatasoft.com/api/explore/v2.1/catalog/datasets/hospitales/records?'

# Obtener la lista completa de hospitales
lista_hospitales = obtener_todos_hospitales(url_api)

# Agrupar hospitales por distrito
hospitales_por_distrito = agrupar_hospitales_por_distrito(lista_hospitales)

# Convertir a JSON y imprimir
json_resultado = json.dumps(hospitales_por_distrito, indent=2, ensure_ascii=False)
print(json_resultado)

# Opcional: guardar en un archivo JSON
with open('hospitales_por_distrito.json', 'w', encoding='utf-8') as f:
    json.dump(hospitales_por_distrito, f, indent=2, ensure_ascii=False)