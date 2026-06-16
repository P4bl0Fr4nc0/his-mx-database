USE his_mx; 

CREATE TABLE contacto_emergencia(
id_contacto_eme INT AUTO_INCREMENT PRIMARY KEY ,
id_paciente INT,
cve_parentesco TINYINT, 
nombre VARCHAR(100) NOT NULL,
apellido_paterno VARCHAR(100) NOT NULL,
apellido_materno VARCHAR(100) NOT NULL,
telefono VARCHAR(20) NOT NULL,
correo VARCHAR(100) NULL,

CONSTRAINT fk_contacto_eme_cat_parentesco
FOREIGN KEY (cve_parentesco)
REFERENCES cat_parentesco(cve_parentesco),

CONSTRAINT fk_contacto_eme_pacientes 
FOREIGN KEY (id_paciente)
REFERENCES pacientes(id_paciente)
);

