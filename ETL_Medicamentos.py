#ETL para carga de catalogo de medicamentos
import pandas as pd
from sqlalchemy import create_engine
import time
import os 
from dotenv import load_dotenv

inicio = time.time()

#Importar archivo excel
df = pd.read_excel("cat_medicamentos.xlsx",
                   sheet_name="cat_medicamentos",                   
                   #Columnas que se usaran 
                   usecols=["sustancia_activa","nombre_comercial","presentacion","concentracion", "via_administracion","activo"],
                     dtype={"sustancia_activa":"string", 
                            "nombre_comercial": "string", 
                            "presentacion":"string",
                            "concentracion":"string",
                            "via_administracion":"string",
                            "activo":"int"
                           }                
)   

#Cantidad de registros extraidos
print (f"Extraidos:{len(df)} registros")

# Imprimir 5 primero y 5 ultimos
print(df.head())
#Informacion del tipo de datos de columnas
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
        
        df.to_sql("cat_medicamentos", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla cat_medicamentos")

        
except Exception as e:

    print(f"Error en ETL: {e} se realizo rollback")
