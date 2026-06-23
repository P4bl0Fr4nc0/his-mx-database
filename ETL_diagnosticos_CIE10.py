#ETL para carga de datos del catalogo CIE-10 correspondiente a la NOM 024

import pandas as pd 
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import time

inicio = time.time()

#Variables para inico de sesion en la base de datos en el archivo .env 
load_dotenv()
usuario = os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASS")
host = os.getenv("MYSQL_HOST")
puerto = os.getenv("MYSQL_PORT")
database = os.getenv("MYSQL_DB_NAME")

#Conexion a la base de datos con su driver y carga de tabla
engine = create_engine(f"mysql+pymysql://{usuario}:{password}@{host}:{puerto}/{database}")

#Importar archivo excel
df_diagnosticos = pd.read_excel("cat_diagnosticos.xlsx",
                   sheet_name="CIE-ABRIL-2024",                   
                   #Columnas que se usaran 
                   usecols=["CATALOG_KEY","NOMBRE","LSEX","CLAVE_CAPITULO","CAPITULO"],
                   dtype={"CATALOG_KEY":"string", 
                          "NOMBRE": "string",
                          "LSEX": "string", 
                          "CLAVE_CAPITULO": "string",
                          "CAPITULO":"string"
                          }
                
)

registros = []

#Mapeo de sexo de a cuerdo a la columna LSEX del catalogo

sexo_map = {
    "NO": 0,
    "HOMBRE": 1,
    "MUJER": 2
}

df_diagnosticos["cve_sexo_aplica"] = (
    df_diagnosticos["LSEX"]
    .str.strip()
    .str.upper()
    .map(sexo_map)
    .fillna(0)
    .astype("int8")   
)

#Se crean los registros de acuerdo a la cantidad de filas liedas desde el excel CIE-10
for fila in df_diagnosticos.itertuples(index=False):
    

    registros.append({
        "cve_cie10": fila.CATALOG_KEY,
        "descripcion": fila.NOMBRE,
        "capitulo": fila.CLAVE_CAPITULO.strip(),
        "descripcion_capitulo": fila.CAPITULO,
        "cve_sexo_aplica": fila.cve_sexo_aplica
      
    })

df = pd.DataFrame(registros)


print("-------Comienza la Carga-------")

#Try catch para hacer rollback en caso de error
try:
    with engine.begin() as conexion:
        if len(df) == 0 :
            raise ValueError("El DataFrame está vacío")
        
        df.to_sql("cat_cie10", 
                  conexion,
                  if_exists="append",
                  index=False)

        #tiempo de finalizacion del proceso
        fin = time.time()
        print(f"Se ha completado el ETL: {len(df)} registros cargados en {round(fin-inicio,2)} segundos")
        print(f"Tabla lista en MySQL en la base de datos: {database} y tabla cat_cie10")
        
except Exception as e:
    print(f"Error en ETL: {e} se realizo rollback")
   
