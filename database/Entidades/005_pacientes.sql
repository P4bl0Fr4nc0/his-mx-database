
USE his_mx; 

CREATE TABLE pacientes (
id_paciente  INT AUTO_INCREMENT PRIMARY KEY, 
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


#agregar columnas de telefonos y correo a pacientes, ademas de segundo nombre y cambiar tipo de dato en primary key a int 
ALTER TABLE pacientes ADD column telefono_principal VARCHAR(20) NOT NULL;
ALTER TABLE pacientes ADD column telefono_secundario VARCHAR(20) NULL;
ALTER TABLE pacientes ADD column correo_electronico VARCHAR(100) NULL;
ALTER TABLE pacientes ADD column segundo_nombre VARCHAR(100) NULL;



#agregar columna tipo de sangre y relacion tabla pacientes con cat_tipo de sangre

ALTER TABLE pacientes ADD COLUMN cve_tipo_sangre TINYINT NOT NULL,
ADD CONSTRAINT fk_paciente_cat_tipo_sangre
FOREIGN KEY (cve_tipo_sangre)
REFERENCES cat_tipo_sangre(cve_tipo_sangre);

# se agrega columna del estatus administrativo en el que se encuentra el paciente, activo, inactivo, suspendido o dado de baja
ALTER TABLE pacientes 
ADD COLUMN cve_estatus_admin TINYINT NOT NULL DEFAULT 1;

ALTER TABLE pacientes
ADD CONSTRAINT fk_paciente_estatus_admin
FOREIGN KEY (cve_estatus_admin)
REFERENCES cat_estatus_administrativo(cve_estatus_admin);


Describe pacientes;

SELECT * FROM pacientes;

Select p.nombre as nombre, p.apellido_paterno, p.apellido_materno, cs.descripcion as sexo , cts.descripcion as tipo_sangre, cte.nombre_estado as estado_nacimiento FROM pacientes p
INNER	JOIN cat_sexo cs
ON cs.cve_sexo = p.cve_sexo
INNER JOIN cat_tipo_sangre cts
ON
cts.cve_tipo_sangre = p.cve_tipo_sangre
INNER JOIN cat_estado cte
ON 
cte.cve_estado = p.cve_estado;
