#ETL para creacion de registros de pacientes con Faker para pruebas de tabla pacientes

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

#Se crean 1500 registros falsos 
for i in range (1500):

    sexo = random.choice([1,2])

    if sexo == 1:  # Masculino
            nombre = fake.first_name_male()
            segundo_nombre = (
             fake.first_name_male()
             if random.random() < 0.85 #solo el 85 % de los pacientes tendran segundo nombre  
             else None
    )
    else:  # Femenino
            nombre = fake.first_name_female()
            segundo_nombre = (
                fake.first_name_female()
                if random.random() < 0.85 #solo el 85 % de los pacientes tendran segundo nombre
                else None
    )  

    registros.append({
        "nombre":nombre,
        "segundo_nombre": segundo_nombre,
        "apellido_paterno": fake.last_name(),
        "apellido_materno": fake.last_name(),
        "fecha_nacimiento": fake.date_of_birth(
            minimum_age=0,
            maximum_age=90
        ),

        "curp": fake.bothify(text='????######??????##').upper(),
        "cve_sexo": sexo,
        "cve_pais": "223",
        "cve_estado": str(random.randint(1,32)).zfill(2),
        "cve_estatus": 1,
        "telefono_principal": fake.numerify("55########"),
        "telefono_secundario": (
            fake.numerify("55########")
            if random.random() < 0.40 #aproximadamente 40% de los pacientes no contara con segundo numero telefonico
            else None
        ),
        "correo_electronico": (
            fake.unique.email()
            if random.random() < 0.85 #aproximadamente 85% de los pacientes contara con email
            else None
        ),
        "cve_tipo_sangre": random.randint(1,9),
        "cve_estatus_admin": 1

    })

df = pd.DataFrame(registros)

print(df.head())


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
        
        df.to_sql("pacientes", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla pacientes")
        
except Exception as e:
    print(f"Error en ETL: {e} se realizo rollback")
   
