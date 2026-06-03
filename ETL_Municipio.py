import pandas as pd
from sqlalchemy import create_engine
import time

import os
from dotenv import load_dotenv


inicio = time.time()
#Importar archivo excel
df = pd.read_excel("cat_municipios.xlsx",
                   sheet_name="Hoja1",                   
                   #Columnas que se usaran 
                   usecols=["EFE_KEY","CATALOG_KEY","MUNICIPIO","CVEGEO"],
                   dtype={"EFE_KEY":"string", 
                          "CATALOG_KEY": "string", 
                          "MUNICIPIO":"string",
                          "CVEGEO": "string"
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
    "EFE_KEY": "cve_estado",
    "CATALOG_KEY": "cve_municipio",
    "MUNICIPIO": "nombre_municipio",
    "CVEGEO": "cve_geostadistica"
})


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
        
        df.to_sql("cat_municipio", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla cat_municipios")

        
except Exception as e:

    print(f"Error en ETL: {e} se realizo rollback")
   


