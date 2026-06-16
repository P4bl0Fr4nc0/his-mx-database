
USE his_mx; 


CREATE TABLE domicilio(
id_domicilio INT AUTO_INCREMENT PRIMARY KEY,
id_paciente INT NOT NULL,
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


