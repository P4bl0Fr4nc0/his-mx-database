#ETL para creacion de registros medicos con libreria faker y hacer pruebas con la entidad medicos

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

registros = []

for i in range (150):

    sexo = random.choice([1,2])

    if sexo == 1:  # Masculino
        nombre = fake.first_name_male()
        segundo_nombre = (
        fake.first_name_male()
        if random.random() < 0.85 #solo el 85 % de los medicos tendra segundo nombre  
        else None
    )
    else:  # Femenino
        nombre = fake.first_name_female()
        segundo_nombre = (
        fake.first_name_female()
        if random.random() < 0.85 #solo el 85 % de los medicos tendra segundo nombre  
        else None
    )  

    if random.random() < 0.20: #Alrededor del 20% de los medicos seran medicos generales 
        cve_especialidad = 1 
    else:  cve_especialidad = random.randint(2,46)


    if cve_especialidad == 1:
        cedula_especialidad = None
    else:
        cedula_especialidad = str(9000000 + i)

    registros.append({
        "nombre": nombre,
        "segundo_nombre": segundo_nombre, 
        "apellido_paterno": fake.last_name(),
        "apellido_materno": fake.last_name(),
        "fecha_nacimiento": fake.date_of_birth(
            minimum_age=28,
            maximum_age=60
        ),

        "curp": fake.bothify(text='????######??????##').upper(),
        "cve_sexo": sexo,
        "cedula_profesional": str(7000000 + i),
        "cve_especialidad": cve_especialidad,
        "cedula_especialidad": cedula_especialidad,
         "telefono": fake.numerify("55########"),
        "correo_electronico": fake.unique.email(),
        "cve_estatus_admin": 1,
        "cve_nacionalidad": '233'

    })

df = pd.DataFrame(registros)

print(df.head())
print(df.dtypes)


print("-------Comienza la Carga-------")

load_dotenv()
usuario = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASS")
host = os.getenv("MYSQL_HOST")
puerto = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DB_NAME")

#Conexion a la base de datos con su driver y carga de tabla
engine = create_engine(f"mysql+pymysql://{usuario}:{password}@{host}:{puerto}/{database}")

#Try catch para hacer rollback en caso de error
try:
    with engine.begin() as conexion:
        if len(df) == 0 :
            raise ValueError("El DataFrame está vacío")
        
        df.to_sql("medicos", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla medicos")
        
except Exception as e:
    print(f"Error en ETL: {e} se realizo rollback")
   
