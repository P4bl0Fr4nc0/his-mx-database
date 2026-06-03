import pandas as pd
from sqlalchemy import create_engine
import time

import os 
from dotenv import load_dotenv


inicio = time.time()
#Importar archivo excel
df = pd.read_excel("cat_estado.xlsx",
                   sheet_name="ENTIDAD_FEDERATIVA",                   
                   #Columnas que se usaran 
                   usecols=["CATALOG_KEY","ENTIDAD_FEDERATIVA","ABREVIATURA"]

)

#Cantidad de registros extraidos
print (f"Extraidos:{len(df)} registros")

# Imprimir 5 primero y 5 ultimos
print(df.head())
#Informacion del tipo de datos de columnas
print(df.info())

#Asignacion de columnas a tabla de MySQL
df = df.rename(columns={
    "CATALOG_KEY": "cve_estado",
    "ENTIDAD_FEDERATIVA": "nombre_estado",
    "ABREVIATURA": "abreviatura"
})


# pasar columna a texto 
df["cve_estado"] = df["cve_estado"].astype("string")

#corregir error del codigo con clave 88 que detecta como vacio cuando es NA No aplica
df.loc[
    df["cve_estado"] == 88,
    "cve_estado"
] = "NA"

print(df.info())
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
        
        df.to_sql("cat_estado", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla cat_nacionalidad")

        
except Exception as e:

    print(f"Error en ETL: {e} se realizo rollback")
   


