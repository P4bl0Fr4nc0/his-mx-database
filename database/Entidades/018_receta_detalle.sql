use his_mx;

CREATE TABLE receta_detalle(
id_detalle INT PRIMARY KEY AUTO_INCREMENT,
id_receta INT NOT NULL,
id_medicamento INT NOT NULL,
dosis VARCHAR(100) NOT NULL,
frecuencia VARCHAR(100) NOT NULL, -- ejemplo: cada 8 horas
duracion VARCHAR (100) NOT NULL, -- ejemplo: 7 días
cantidad INT NOT NULL, -- ejemplo 2 frascos, paquetes etc
indicaciones TEXT NULL,
fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
CONSTRAINT fk_receta_detalle_receta
FOREIGN KEY (id_receta) REFERENCES recetas(id_receta),
CONSTRAINT fk_receta_detalle_medicamentos
FOREIGN KEY (id_medicamento) REFERENCES cat_medicamentos(id_medicamento)
);