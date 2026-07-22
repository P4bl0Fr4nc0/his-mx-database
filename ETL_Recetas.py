#ETL para creacion de registros de recetas
import pandas as pd 
import random
from faker import Faker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import time

inicio = time.time()

#Definir el idioma en que quiero que me cree los datos
fake = Faker("es_MX")

#Variables para inico de sesion en la base de datos en el archivo .env 
load_dotenv()
usuario = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASS")
host = os.getenv("MYSQL_HOST")
puerto = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DB_NAME")

#Conexion a la base de datos con su driver y carga de tabla
engine = create_engine(f"mysql+pymysql://{usuario}:{password}@{host}:{puerto}/{database}")

#seleccionar id de consulta de tabla consultas
df_consultas= pd.read_sql("""
SELECT
    id_consulta, 
    id_medico,
    fecha_consulta
FROM consultas 
""", engine)

#seleccionar id medico para recetas donde el medico que dio la consulta no sea el mismo que emite receta
df_medicos = pd.read_sql("""
SELECT
    id_medico
FROM consultas 
""", engine)

consultas = df_consultas.sample(n=100, replace=True).reset_index(drop=True)

registros = []

#Se crean 100 consultas aleatorias tomadas de muestra
for _, consulta in consultas.iterrows():
          
    # 70% de probabilidad que la receta sea emitida por el mismo médico que dio a consulta
    # 30% que sea emitida por otro médico del hospital
    if random.random() < 0.7:
        medico_receta = consulta["id_medico"]
    else:
        medico_receta = df_medicos.sample(1).iloc[0]["id_medico"]

    registros.append({
        "id_consulta": consulta["id_consulta"],
        "id_medico": medico_receta,        
        "fecha_emision": consulta["fecha_consulta"], #se mantiene la fecha de consulta como fecha de emision para pruebas     
        "indicaciones_generales": fake.text(max_nb_chars= 10), #texto aleatorio solo para pruebas            
    })       
    
df = pd.DataFrame(registros)    

print(df.head(10))

print("-------Comienza la Carga-------")

#Try catch para hacer rollback en caso de error
try:
    with engine.begin() as conexion:
        if len(df) == 0 :
            raise ValueError("El DataFrame está vacío")
        
        df.to_sql("recetas", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla recetas")
        
except Exception as e:
    print(f"Error en ETL: {e} se realizo rollback")