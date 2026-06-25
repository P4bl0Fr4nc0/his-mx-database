#ETL para creacion de registros de consultorios de acuerdo a las especialidades existentes 
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

df_especialidades = pd.read_sql("""
SELECT
    cve_especialidad,
    descripcion
FROM cat_especialidad
""", engine)


registros = []
contador_edificio = { #contador de consultorios de  cada edificios
        1: 1,
        2: 1
        }

#Se crean los registros de acuerdo a la cantidad de claves de cve_especialidad leidas
for _, row in df_especialidades.iterrows():       
        
        edificio = random.randint(1, 2) #solo existiran dos edificios

        numero_consultorio = edificio * 100 + contador_edificio[edificio] # se convierte el edificio en 100 y se le suma el contador

        registros.append({
        "nombre": row["descripcion"],
        "ubicacion": f"Edificio {edificio}",
        "numero_consultorio": numero_consultorio
        })

        contador_edificio[edificio] += 1

df = pd.DataFrame(registros)

print(df.head())


print("-------Comienza la Carga-------")

#Try catch para hacer rollback en caso de error
try:
    with engine.begin() as conexion:
        if len(df) == 0 :
            raise ValueError("El DataFrame está vacío")
        
        df.to_sql("consultorios", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla consultorios")
        
except Exception as e:
    print(f"Error en ETL: {e} se realizo rollback")
