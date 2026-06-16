USE his_mx; 

#Creacion de tabla médicos

CREATE TABLE medicos (
    id_medico INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    segundo_nombre VARCHAR(100) NULL,
    apellido_paterno VARCHAR(100) NOT NULL,
    apellido_materno VARCHAR(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
	curp CHAR(18) NULL UNIQUE,
	cve_sexo TINYINT NOT NULL,
    cedula_profesional VARCHAR(20) NOT NULL UNIQUE,
    cve_especialidad TINYINT NOT NULL,
	cedula_especialidad VARCHAR(20) NULL UNIQUE,    
    telefono VARCHAR(20) NOT NULL,
    correo_electronico VARCHAR(100) NULL UNIQUE,
    cve_estatus_admin TINYINT NOT NULL DEFAULT 1,
    cve_nacionalidad CHAR(3) NOT NULL,
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_medico_especialidad
    FOREIGN KEY (cve_especialidad)
    REFERENCES cat_especialidad(cve_especialidad),
    
    CONSTRAINT fk_medico_estatus
    FOREIGN KEY (cve_estatus_admin)
    REFERENCES cat_estatus_administrativo(cve_estatus_admin),
    
    CONSTRAINT fk_medico_sexo
	FOREIGN KEY (cve_sexo)
	REFERENCES cat_sexo(cve_sexo),
    
    CONSTRAINT fk_medico_nacionalidad
    FOREIGN KEY (cve_nacionalidad)
    REFERENCES cat_nacionalidad(cve_nacionalidad)
);

/*
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE medicos;
SET FOREIGN_KEY_CHECKS = 1;
*/
SELECT * FROM medicos;

#Consulta para checar los medicos y la especialidad que se le asigno con faker

SELECT m.id_medico, m.nombre, m.segundo_nombre, m.cve_especialidad, ce.descripcion FROM medicos m
INNER JOIN cat_especialidad ce
ON  ce.cve_especialidad = m.cve_especialidad;


Select * from medicos;

# Consulta para ver nombre, apelludo, nacionalidad y especialidad del médico
SELECT m.nombre, m.apellido_paterno as apellido, cn.nombre_pais  as nacionalidad, ce.descripcion as especialidad FROM medicos m
INNER JOIN cat_nacionalidad cn
ON m.cve_nacionalidad = cn.cve_nacionalidad
INNER JOIN cat_especialidad ce 
ON m.cve_especialidad = ce.cve_especialidad;
    



