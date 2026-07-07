#ETL para creacion de registros de diagnosticos
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

#seleccionar columnas er la tabla consultas
df_consultas = pd.read_sql("""
SELECT
    id_consulta
FROM consultas 
""", engine)

#seleccionar columnas de tabla cat_diagnosticos
df_diagnostico = pd.read_sql("""                             
SELECT 
    cve_cie10
FROM cat_cie10                           
""",engine)

consultas = df_consultas.copy().reset_index(drop=True)

registros = []

codigos_excluir = ['A34X', 'B373', 'B260', '9999'] # Codigos CIE-10 a excluir ya que son exclusivos para sexo femenino y no se requieren para las pruebas.

df_diagnostico = df_diagnostico[~df_diagnostico["cve_cie10"].isin(codigos_excluir)]

#Se crean consultas 
for _, paciente in consultas.iterrows():
          
    diagnosticos = df_diagnostico.sample(1).iloc[0]
  
    registros.append({
        "id_consulta": paciente["id_consulta"], 
        "cve_cie10": diagnosticos["cve_cie10"],       
        "tipo_diagnostico":random.choice(['inicial', 'definitivo', 'diferencial']),
                
    })       
    
df = pd.DataFrame(registros)    

print(df.head(10))


print("-------Comienza la Carga-------")

#Try catch para hacer rollback en caso de error
try:
    with engine.begin() as conexion:
        if len(df) == 0 :
            raise ValueError("El DataFrame está vacío")
        
        df.to_sql("diagnosticos", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla diagnosticos")
        
except Exception as e:
    print(f"Error en ETL: {e} se realizo rollback")

