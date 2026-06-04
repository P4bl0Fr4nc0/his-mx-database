/* Catalogos nacionalidad, estado, municipio, localidad
de acuerdo con los catalogos de la nom-024-ssa3
*/

USE his_mx; 

CREATE TABLE cat_nacionalidad (
cve_nacionalidad CHAR(3) PRIMARY KEY,
nombre_pais VARCHAR(100) NOT NULL,
abreviatura CHAR(3) NULL UNIQUE
);


CREATE TABLE cat_estado (
cve_estado CHAR(2) PRIMARY KEY NOT NULL,
nombre_estado VARCHAR(100) NOT NULL,
abreviatura CHAR(3) NOT NULL
);

CREATE TABLE cat_municipio(
cve_estado CHAR (2) NOT NULL,
cve_municipio CHAR(3) NOT NULL,
nombre_municipio VARCHAR(100) NOT NULL,
cve_geostadistica char(5) NOT NULL UNIQUE,

PRIMARY KEY (cve_estado, cve_municipio),

CONSTRAINT fk_municipio_estado
	FOREIGN KEY (cve_estado)
    REFERENCES cat_estado(cve_estado)
);

CREATE TABLE cat_localidad(
cve_estado CHAR(2) NOT NULL,
cve_municipio CHAR(3) NOT NULL,
cve_localidad CHAR(4) NOT NULL,
nombre_localidad VARCHAR(100) NOT NULL,
cve_geostadistica CHAR(9) NOT NULL UNIQUE,

PRIMARY KEY(
cve_estado,
cve_municipio,
cve_localidad
), 

CONSTRAINT fk_localidad_municipio
FOREIGN KEY ( 
cve_estado,
cve_municipio)
REFERENCES cat_municipio(
cve_estado,
cve_municipio)
);


/*  Eliminacion de registros por correccion de datos y columnas en ETL
SET FOREIGN_KEY_CHECKS = 0;
Truncate TABLE cat_nacionalidad;
Truncate TABLe pacientes;
Truncate TABLE cat_estado;
truncate TABLE cat_municipio;
Truncate TABLE cat_localidad;
SET FOREIGN_KEY_CHECKS = 1;
*/
