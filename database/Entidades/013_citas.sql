USE his_mx; 
#Creacion de entidad citas
CREATE TABLE citas (
    id_cita INT AUTO_INCREMENT PRIMARY KEY,
    id_expediente INT NOT NULL, 
    id_medico INT NOT NULL,
    id_consultorio INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    cve_estatus_cita TINYINT NOT NULL,
    motivo TEXT,
	fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, #auditoria

	CONSTRAINT fk_citas_expediente
    FOREIGN KEY (id_expediente) REFERENCES expedientes(id_expediente),
    CONSTRAINT fk_citas_medico
    FOREIGN KEY (id_medico) REFERENCES medicos(id_medico),
    CONSTRAINT fk_citas_consultorio
	FOREIGN KEY (id_consultorio) REFERENCES consultorios(id_consultorio),
    CONSTRAINT fk_citas_cat_status_cita
	FOREIGN KEY (cve_estatus_cita) REFERENCES cat_estatus_cita(cve_estatus_cita),
    
	#Creacion de indices para una mejor busqueda de registros ya que las citas suelen ser muchas 
    INDEX idx_citas_expediente (id_expediente),
	INDEX idx_citas_medico (id_medico),
	INDEX idx_citas_consultorio (id_consultorio),
    INDEX idx_citas_fecha (fecha_hora)
    
 );

	
    
    