#ETL para creacion de registros de pacientes con Faker para pruebas de tabla domicilio#ETL para creacion de registros de pacientes con Faker para pruebas de tabla pacientes

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

df_localidades = pd.read_sql("""
SELECT
    cve_estado,
    cve_municipio,
    cve_localidad
FROM cat_localidad
""", engine)

df_pacientes = pd.read_sql("""
SELECT id_paciente
FROM pacientes
""", engine)

registros = []


# Escoge una localidad válida

#Se crean los registros de acuerdo a la cantidad de id leidos desde la base de datos aplicable tambien al ETL de contactos de emergencia
for id_paciente in df_pacientes["id_paciente"]:
    

    ubicacion = df_localidades.sample(1).iloc[0]

    ubicacion["cve_estado"]     
    ubicacion["cve_municipio"]  
    ubicacion["cve_localidad"]  

    registros.append({
        "id_paciente":id_paciente,
        "calle": fake.street_name(),
        "num_ext": random.randint(1, 2000),
        "num_int": (
             random.randint(1, 50)
             if random.random() < 0.30 #Al menos el 30# de las direcciones tendran numero interior
            else None
        ),
        "colonia": fake.city_suffix(), 
        "cp": f"{random.randint(0, 99999):05d}",
        "cve_estado": ubicacion["cve_estado"],
        "cve_municipio": ubicacion["cve_municipio"],
        "cve_localidad": ubicacion["cve_localidad"],

        "fecha_fin_vigencia": None
              
    })


df = pd.DataFrame(registros)

print(df.head())

print("-------Comienza la Carga-------")


#Try catch para hacer rollback en caso de error
try:
    with engine.begin() as conexion:
        if len(df) == 0 :
            raise ValueError("El DataFrame está vacío")
        
        df.to_sql("domicilio", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla domicilio")
        
except Exception as e:
    print(f"Error en ETL: {e} se realizo rollback")
   
