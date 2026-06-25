#ETL para creacion de registros de consultorios de acuerdo a las especialidades existentes 
import pandas as pd 
import random
from faker import Faker
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import time
from datetime import datetime

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

df_pacientes = pd.read_sql("""
SELECT
    id_paciente, cve_sexo
FROM pacientes ORDER BY id_paciente
""", engine)

registros = []

numero_expediente = 1

#Se crean los registros de acuerdo a la cantidad de claves de cve_especialidad leidas
for _, row in df_pacientes.iterrows(): 
      
        # se determina si el paciente es masculino o femenino para agregar antecedentes gincecoobstetricos

        if row["cve_sexo"] == 1:
            antecedentes_ginecoobstetricos = ""
        elif row["cve_sexo"] == 2:
         antecedentes_ginecoobstetricos = fake.text(max_nb_chars=150) 
        else :
         antecedentes_ginecoobstetricos = None

        #Ojo: los textos son aleatorios y no tienen nada que ver con textos medicos, unicamente son para pruebas de campos
        registros.append({
        "id_paciente":row["id_paciente"],
        "id_medico": random.randint(1,150), #id de medicos que existen se deben cuidar los id dados de alta en base de datos
        "numero_expediente": str(numero_expediente).zfill(5), #se tendran 5 caracteres en numero de expediente, se llenaran con ceros los que no tengan digito
        "antecedentes_heredofamiliares": fake.text(max_nb_chars= 100),
        "antecedentes_personales_no_patologicos":  (
            fake.text(max_nb_chars= 40)
            if random.random() < 0.20 #aproximadamente 40% de los pacientes tendran antecedentes personales no patologicos  
            else None ),
        "antecedentes_personales_patologicos": (
            fake.text(max_nb_chars= 50)
            if random.random() < 0.20 #aproximadamente 30% de los pacientes tendran antecedentes personales patologicos
            else None ),
        "antecedentes_ginecoobstetricos": antecedentes_ginecoobstetricos,
        "alergias": (
            fake.text(max_nb_chars= 20)
            if random.random() < 0.20 #aproximadamente 20% de los pacientes tendran alergias
            else None ),
        "padecimientos_cronicos": (
            fake.text(max_nb_chars= 50)
            if random.random() < 0.30 #aproximadamente 30% de los pacientes tendran padecimientos cronicos
            else None ),
        "discapacidades":  (
            fake.text(max_nb_chars= 30)
            if random.random() < 0.05 #aproximadamente 5% de los pacientes tendra una discapacidad
            else None ), 
        "cirugias_previas":  (
            fake.text(max_nb_chars= 30)
            if random.random() < 0.10 #aproximadamente 10% de los pacientes tendra una cirugia previa
            else None ), 
        "transfusiones":  (
            fake.text(max_nb_chars= 30)
            if random.random() < 0.02 #aproximadamente 2% de los pacientes tuvo alguna transfusion
            else None ), 
        "fecha_apertura": datetime.now(),    
        "cve_estatus_admin": 1
        })
        
        numero_expediente += 1

df = pd.DataFrame(registros)

print(df.head(10))

print("-------Comienza la Carga-------")

#Try catch para hacer rollback en caso de error
try:
    with engine.begin() as conexion:
        if len(df) == 0 :
            raise ValueError("El DataFrame está vacío")
        
        df.to_sql("expedientes", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla expedientes")
        
except Exception as e:
    print(f"Error en ETL: {e} se realizo rollback")

