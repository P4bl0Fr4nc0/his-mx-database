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

    cve_parentesco = random.choices(#Probabilidad que los parentescos de Padre, Madre, Coyuge, Hijo aparezcan mas veces
    population=[1,2,3,4,5,6,7,8],
    weights=[20,20,15,15,10,10,5,5],
    k=1
    )[0]

    sexo = random.choice(["M", "F"])  #determinar sexo para que me obtenga los nombres masculino y femeninos correctamente

    if sexo == "M":
        nombre = fake.first_name_male()
        segundo_nombre = (
            fake.first_name_male()
            if random.random() < 0.80
            else None
        )
    else:
        nombre = fake.first_name_female()
        segundo_nombre = (
            fake.first_name_female()
            if random.random() < 0.80
            else None
        )
    
    registros.append({

        "cve_parentesco": cve_parentesco,
        "id_paciente": i+1, #va del id al 1500 de acuerdo con el ETL de pacientes, si los ids son diferentes tendra que hacerse la numeracion correspondiente
        "nombre":nombre,
        "segundo_nombre":segundo_nombre,
        "apellido_paterno": fake.last_name(),
        "apellido_materno": fake.last_name(),        
        "telefono": fake.numerify("55########"),
        "correo_electronico": (
            fake.unique.email()
            if random.random() < 0.85 #aproximadamente 85% de contactos de emergencia contaran con email
            else None
        ),
       
    })

df = pd.DataFrame(registros)

print(df.head(100))

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
        
        df.to_sql("contacto_emergencia", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla contactos de emergencia")
        
except Exception as e:
    print(f"Error en ETL: {e} se realizo rollback")
   
