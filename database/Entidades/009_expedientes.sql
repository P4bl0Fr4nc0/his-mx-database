USE his_mx; 

#Creacion de tabla expedientes

CREATE TABLE expedientes (
    id_expediente       INT AUTO_INCREMENT PRIMARY KEY,
    id_paciente         INT NOT NULL UNIQUE,
    id_medico INT NOT NULL,  #medico responsable para abrir expediente
    numero_expediente   VARCHAR(20) NOT NULL UNIQUE,    
    antecedentes_heredofamiliares TEXT NULL,
    antecedentes_personales_no_patologicos TEXT NULL,
    antecedentes_personales_patologicos TEXT NULL,
    antecedentes_ginecoobstetricos TEXT NULL, #Para mujeres
    alergias TEXT NULL,
    padecimientos_cronicos TEXT NULL,
    discapacidades TEXT NULL,
	cirugias_previas TEXT NULL,
	transfusiones TEXT NULL,
    fecha_apertura       DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cve_estatus_admin     TINYINT NOT NULL DEFAULT 1,

    CONSTRAINT fk_expediente_paciente
    FOREIGN KEY (id_paciente)
    REFERENCES pacientes(id_paciente),

    CONSTRAINT fk_expediente_estatus
    FOREIGN KEY (cve_estatus_admin)
    REFERENCES cat_estatus_administrativo(cve_estatus_admin),
    
    CONSTRAINT fk_expediente_medico
	FOREIGN KEY (id_medico)
	REFERENCES medicos(id_medico)
);

