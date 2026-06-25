
#Creacion de la entidad consultas
USE his_mx; 

CREATE TABLE consultas (
    id_consulta INT AUTO_INCREMENT PRIMARY KEY,
    id_cita INT NULL,
    id_expediente INT NOT NULL,
    id_medico        INT NOT NULL,
    fecha_consulta   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_consulta ENUM('Cita','Urgencia','Externa') NOT NULL,  
    motivo_consulta  TEXT NOT NULL,
    exploracion_fisica TEXT NULL,
    nota_medica      TEXT NOT NULL,
    plan_tratamiento TEXT NULL,
    fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    INDEX idx_consultas_cita (id_cita),
    
    CONSTRAINT fk_consultas_expediente
    FOREIGN KEY (id_expediente) REFERENCES expedientes(id_expediente),
	CONSTRAINT fk_consultas_citas
    FOREIGN KEY (id_cita) REFERENCES citas(id_cita),
    CONSTRAINT fk_consultas_medico
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico)
);