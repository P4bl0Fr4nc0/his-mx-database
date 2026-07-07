#ETL para creacion de registros de consultas
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

#seleccionar columnas de la tabla medicos
df_expediente = pd.read_sql("""
SELECT
    id_expediente
FROM expedientes 
""", engine)

#seleccionar columnas de la tabla consultorios
df_medicos = pd.read_sql("""                             
SELECT 
    id_medico
FROM medicos                           
""",engine)

expedientes = df_expediente.sample(n=100, replace=True).reset_index(drop=True)

registros = []

#Se crean 100 consultas aleatorias tomadas de muestra
for _, paciente in expedientes.iterrows():
          
    medico = df_medicos.sample(1).iloc[0]
  
    registros.append({
        "id_cita": None, # no se hace cruce con citas ya uqe son consultas realizadas en fecha actual
        "id_expediente": paciente["id_expediente"],
        "id_medico": medico["id_medico"],
        "fecha_consulta":  fake.date_time_between(
        start_date="-30d",   # desde hace 30 días
        end_date="now"       # hasta hoy
        ),
        "tipo_consulta":random.choice(['Cita', 'Urgencia', 'Externa']),
        "motivo_consulta": fake.text(max_nb_chars= 30),
        "exploracion_fisica": fake.text(max_nb_chars= 30),
        "nota_medica": fake.text(max_nb_chars= 30),
        "plan_tratamiento": fake.text(max_nb_chars= 30)         
           
    })       
    
df = pd.DataFrame(registros)    

print(df.head(10))

print("-------Comienza la Carga-------")

#Try catch para hacer rollback en caso de error
try:
    with engine.begin() as conexion:
        if len(df) == 0 :
            raise ValueError("El DataFrame está vacío")
        
        df.to_sql("consultas", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla consultas")
        
except Exception as e:
    print(f"Error en ETL: {e} se realizo rollback")

