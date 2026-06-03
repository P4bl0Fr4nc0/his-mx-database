import pandas as pd
from sqlalchemy import create_engine
import time

import os 
from dotenv import load_dotenv


inicio = time.time()
#Importar archivo excel
df = pd.read_excel("Cat_nacionalidades.xlsx",
                   sheet_name="Hoja1",                   
                   #Columnas que se usaran 
                   usecols=["codigo pais","pais","clave nacionalidad"],
                   dtype={"codigo pais":"string", 
                          "pais": "string", 
                          "clave nacionalidad":"string"
                          }
                
)

#Cantidad de registros extraidos
print (f"Extraidos:{len(df)} registros")

# Imprimir 5 primero y 5 ultimos
print(df.head())
#Informacion del tipo de datos de columnas
print(df.info())

#Asignacion de columnas a tabla de MySQL
df = df.rename(columns={
    "codigo pais": "cve_pais",
    "pais": "nombre_pais",
    "clave nacionalidad": "abreviatura"
})

#limpiar espacion si es que los hay 
df["cve_pais"] = df["cve_pais"].str.strip()
df["nombre_pais"] = df["nombre_pais"].str.strip()


# Corrección de inconsistencia detectada en catálogo NOM-024
# Se elimina el registro "AMERICANA" (código 299)
# debido a que comparte la clave USA con "ESTADOUNIDENSE"
# y genera conflicto con la PK cve_pais.

df = df[df["nombre_pais"] != "AMERICANA"]


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
        
        df.to_sql("cat_nacionalidad", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla cat_nacionalidad")

        
except Exception as e:

    print(f"Error en ETL: {e} se realizo rollback")
   
