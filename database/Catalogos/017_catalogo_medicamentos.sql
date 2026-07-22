use his_mx;

CREATE TABLE cat_medicamentos(

id_medicamento INT PRIMARY KEY AUTO_INCREMENT,
sustancia_activa VARCHAR(150) NOT NULL, -- ejemplo: paracetamol
nombre_comercial VARCHAR(150) NULL, -- ejemplo: Tempra
presentacion VARCHAR(100) NOT NULL, -- ejemplo: tableta, jarabe, inyectable etc.
concentracion VARCHAR(50) NOT NULL, -- ejemplo 500 mg, 1 g 
via_administracion VARCHAR(50) NOT NULL, -- oral, intravenosa etc
activo TINYINT NOT NULL DEFAULT 1,
fecha_registro DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);