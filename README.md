<h3>Hola! Somos el equipo DP1<br><br>Raúl Algora, Marc Cantero, Claudia Romero, Ting Wang</h3>
<br>
<br>
A continuación te doy una breve descripción de lo que encontrarás en este repositorio:
<br>
<h4>BBDD</h4>
En esta carpeta podrás encontrar cada uno de los archivos ".py" que cogen mediante API u otros metodos en algunos casos la información que utilizaremos como base de datos, la limpian mediante el uso de ciertas librerías para finalmente enviarla a Postgres.
<br>
<h4>OLD</h4>
En esta carpeta hemos querido dejar algunos de nuestros primeros archivos que han terminado convirtiendose en lo que es ahora el proyecto. Estos son "mapa2 copy.py", una versión exitosa de nuestro mapa de streamlit y "metro_to_distrito.py" donde realizamos un codigo para transformar la información de las bocas de metro, las cuales no contenia el distrito sino las coordenadas geograficas, y mediante la libreria shapely, lo comparabamos con las coordenadas de distritos y generabamos en la informacion final una columna nueva con el nombre del distrito en el que se ubicaba cada boca de metro.
<br>
<h4>POSTGRES</h4>
En esta carpeta podrás encontrar el "query.py", el cual utilizando la libreria psicopg2, coge toda la información de las bases de datos a través de postgres, las cuales estan divididas en tablas, y genera en el mismo servidor, una tabla nueva que mediante el uso de JOINS recopila toda la informacion necesaria para que expondremos posteriormente en el mapa.
<br>
<h4>mapa_sqlito.py</h4>
El archivo de python que finalmente haciendo uso de la tabla que se ha creado anteriormente, genera mediante streamlit el producto final.
<br>
<h4>orquest_luigi.py</h4>
El archivo de python que haciendo uso de Luigi, nos ayuda como "orchestrator" para la automatización de todos los procesos, dando un orden y unas prioridades según convenga.
<br>
<h4>servers.json</h4>
Archivo JSON necesario para la generación automatizada de un servidor en posgres/pgadmin.
<br>
<br>
Para poder ejecutar nuestro proyecto, por favor, siga estos pasos:
<br>
<br>
1. Ejecutar el archivo docker-compose.yml: docker compose up -d<br>
2. Si quieres ver la base de datos, puede estrar en pgAdmin4 http://localhost:5050 e inicia sesión<br>
&nbsp&nbsp&nbsp&nbsp- User: pgadmin4@pgadmin.org<br>
&nbsp&nbsp&nbsp&nbsp- Password: admin<br>
4. Despliega los servidores y verás que hay un servidor creado! Introduzca la contraseña: Welcome01<br>
5. En unos segundos te saldrá la base de datos SQL.<br>
6. Ahora, si quieres ver el mapa final, accede a streamlit: http://localhost:8501/<br>
<br>
Finalmente, para ver el proyecto en funcionamiento, puedes acceder a este enlace y visualizar un breve video: https://www.youtube.com/watch?v=IK-wb__eD2I 
<br>
