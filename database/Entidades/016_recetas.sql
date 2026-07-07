
USE his_mx;

CREATE TABLE recetas (
id_receta INT PRIMARY KEY AUTO_INCREMENT,
id_consulta INT NOT NULL,
id_medico INT NOT NULL,
fecha_emision DATE NOT NULL,
indicaciones_generales TEXT NOT NULL,
fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

CONSTRAINT fk_recetas_consultas
FOREIGN KEY (id_consulta) REFERENCES consultas(id_consulta),
CONSTRAINT fk_recetas_medico
FOREIGN KEY (id_medico) REFERENCES medicos(id_medico)
);