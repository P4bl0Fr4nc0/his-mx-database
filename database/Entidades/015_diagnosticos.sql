
#Creacion de la entidad diagnosticos

USE his_mx; 

CREATE TABLE diagnosticos (
    id_diagnostico  INT AUTO_INCREMENT PRIMARY KEY,
    id_consulta INT NOT NULL,
    cve_cie10 VARCHAR(10) NOT NULL,
    tipo_diagnostico ENUM('inicial','definitivo','diferencial') NOT NULL,
    fecha_registro   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_diagnostico_consulta
    FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta),

    CONSTRAINT fk_diagnostico_cie10
    FOREIGN KEY (cve_cie10) REFERENCES cat_cie10(cve_cie10)
);