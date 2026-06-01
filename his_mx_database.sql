CREATE DATABASE his_mx char set utf8mb4 collate utf8mb4_0900_ai_ci;

USE his_mx; 

/* Catalogos nacionalidad, estado, municipio, localidad
de acuerdo con los catalogos de la nom-024-ssa3
*/
CREATE TABLE cat_nacionalidad (
cve_pais CHAR(3) PRIMARY KEY,
nombre_pais VARCHAR(100) NOT NULL,
codigo_pais SMALLINT NOT NULL UNIQUE
);


CREATE TABLE cat_estado (
cve_estado CHAR(2) PRIMARY KEY,
nombre_estado VARCHAR(100) NOT NULL
);

CREATE TABLE cat_municipio(
cve_estado CHAR (2) NOT NULL,
cve_municipio CHAR(3) NOT NULL,
nombre_municipio VARCHAR(100) NOT NULL,

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

#catalogos sexo y estatus del paciente
CREATE TABLE cat_sexo(
cve_sexo TINYINT PRIMARY KEY,
descripcion VARCHAR (20) NOT NULL
);

CREATE TABLE cat_estatus_paciente(
    cve_estatus TINYINT PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL
);


CREATE TABLE pacientes (
id_paciente  BIGINT AUTO_INCREMENT PRIMARY KEY, 
nombre VARCHAR(100) NOT NULL ,
apellido_paterno VARCHAR(100) NOT NULL,
apellido_materno VARCHAR(100) NOT NULL,
fecha_nacimiento DATE NOT NULL,
curp CHAR (18) UNIQUE NOT NULL,
cve_sexo TINYINT NOT NULL,
cve_pais CHAR(3) NOT NULL, #pais de nacimiento
cve_estado CHAR(2) NOT NULL, # estado de nacimieto
cve_estatus TINYINT NOT NULL,
fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,


CONSTRAINT fk_paciente_pais
FOREIGN KEY( cve_pais)
REFERENCES 
cat_nacionalidad(cve_pais),

CONSTRAINT fk_paciente_estado
FOREIGN KEY ( cve_estado)
REFERENCES cat_estado(cve_estado),

CONSTRAINT fk_paciente_sexo
FOREIGN KEY  (cve_sexo)
REFERENCES cat_sexo(cve_sexo),

CONSTRAINT fk_paciente_estatus
FOREIGN KEY  (cve_estatus)
REFERENCES cat_estatus_paciente(cve_estatus)
);


CREATE TABLE domicilio(
domicilio_id BIGINT AUTO_INCREMENT PRIMARY KEY,
id_paciente BIGINT NOT NULL,
calle VARCHAR(150) NOT NULL,
num_ext VARCHAR(20) NOT NULL,
num_int VARCHAR(20) NULL,
colonia VARCHAR(150) NOT NULL,
cp CHAR(5) NOT NULL,
cve_estado char(2) NOT NULL, #estado de residencia
cve_municipio CHAR(3) NOT NULL, # municipio de residencia
cve_localidad CHAR(4) NOT NULL, # localidad de residencia
fecha_inicio_vigencia DATE NOT NULL,
fecha_fin_vigencia DATE NULL,
fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,


CONSTRAINT fk_domicilio_paciente
FOREIGN KEY (id_paciente)
REFERENCES pacientes(id_paciente),

CONSTRAINT fk_domicilio_estado
FOREIGN KEY (cve_estado)
REFERENCES cat_estado(cve_estado),

CONSTRAINT fk_domicilio_municipio
FOREIGN KEY (cve_estado, cve_municipio)
REFERENCES cat_municipio(cve_estado, cve_municipio),

CONSTRAINT fk_domicilio_localidad
FOREIGN KEY (cve_estado, cve_municipio, cve_localidad)
REFERENCES cat_localidad(cve_estado, cve_municipio, cve_localidad)
);



Select * from cat_nacionalidad;



