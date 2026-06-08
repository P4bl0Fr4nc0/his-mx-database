USE his_mx; 

#Creacion de tabla médicos

CREATE TABLE medicos (
    cve_medico      INT AUTO_INCREMENT PRIMARY KEY,
    nombre          VARCHAR(100) NOT NULL,
    segundo_nombre  VARCHAR(100) NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    cedula_profesional VARCHAR(20) NOT NULL UNIQUE,
	cedula_especialidad VARCHAR(20) NULL UNIQUE,
    cve_especialidad SMALLINT NOT NULL,
    telefono        VARCHAR(20) NOT NULL,
    correo          VARCHAR(100) NOT NULL UNIQUE,
    cve_estatus_admin TINYINT NOT NULL DEFAULT 1,
    fecha_registro  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_medico_especialidad
    FOREIGN KEY (cve_especialidad)
    REFERENCES cat_especialidad(cve_especialidad),
    
    CONSTRAINT fk_medico_estatus
    FOREIGN KEY (cve_estatus_admin)
    REFERENCES cat_estatus_administrativo(cve_estatus_admin)
);