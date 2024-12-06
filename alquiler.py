import pandas as pd
import requests
import openpyxl
import json

from distritos_nomeclatura import *


excel_url = "https://cdn.mivau.gob.es/portal-web-mivau/vivienda/serpavi/2024-05-07_bd_sistema-indices-alquiler-vivienda_2011-2022.xlsx"

response = requests.get(excel_url)
with open("2024-05-07_bd_sistema-indices-alquiler-vivienda_2011-2022.xlsx", "wb") as file:
    file.write(response.content)

df_header = pd.read_excel("2024-05-07_bd_sistema-indices-alquiler-vivienda_2011-2022.xlsx", 
                          sheet_name="Distritos",
                          usecols="D, E, HZ, IC",
                          nrows=1,
                          header=0)

df_data = pd.read_excel("2024-05-07_bd_sistema-indices-alquiler-vivienda_2011-2022.xlsx", 
                   sheet_name="Distritos", 
                   usecols="D, E, HZ, IC",
                   skiprows=8992,
                   nrows=19,
                   header=0
                   )

df_data.columns = df_header.columns


# cudis_name = {
#     4625001: {'name': 'CIUTAT VELLA', 'district': 1},
#     4625002: {'name': "L'EIXAMPLE", 'district': 2},
#     4625003: {'name': 'EXTRAMURS', 'district': 3},
#     4625004: {'name': 'CAMPANAR', 'district': 4},
#     4625005: {'name': 'LA SAIDIA', 'district': 5},
#     4625006: {'name': 'EL PLA DEL REAL', 'district': 6},
#     4625007: {'name': "L'OLIVERETA", 'district': 7},
#     4625008: {'name': 'PATRAIX', 'district': 8},
#     4625009: {'name': 'JESUS', 'district': 9},
#     4625010: {'name': 'QUATRE CARRERES', 'district': 10},
#     4625011: {'name': 'POBLATS MARITIMS', 'district': 11},
#     4625012: {'name': 'CAMINS AL GRAU', 'district': 12},
#     4625013: {'name': 'ALGIROS', 'district': 13},
#     4625014: {'name': 'BENIMACLET', 'district': 14},
#     4625015: {'name': 'RASCANYA', 'district': 15},
#     4625016: {'name': 'BENICALAP', 'district': 16},
#     4625017: {'name': 'POBLES DEL NORD', 'district': 17},
#     4625018: {'name': "POBLES DE L'OEST", 'district': 18},
#     4625019: {'name': 'POBLES DEL SUD', 'district': 19}
# }
    

df_data['CUDIS'] = df_data['CUDIS'].map(cudis_name).fillna(df_data['CUDIS'])

# Crear CSV
# df_data.to_csv('alquileres_distritos.csv', index=False)

# Crear JSON
grouped_data = df_data[['LITMUN', 'CUDIS', 'ALQTBID12_M_VC_22', 'ALQTBID12_M_VU_22']].groupby('LITMUN').apply(
    lambda group: group[['CUDIS', 'ALQTBID12_M_VC_22', 'ALQTBID12_M_VU_22']].to_dict(orient='records')
).reset_index(name='cudis_data')
json_data = grouped_data.to_dict(orient='records')

with open('alquileres_distritos.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)


print("Archivo descargado y convertido a CSV y JSON")

