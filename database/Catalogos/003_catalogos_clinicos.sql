
#Catalogo estatus vital del paciente 

CREATE TABLE cat_estatus_paciente(
    cve_estatus TINYINT PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL
);
INSERT INTO cat_estatus_paciente VALUES
(1,'Vivo'),
(2,'Fallecido'),
(3,'Desconocido');

#Catalogo tipo de sangre del paciente 

CREATE TABLE cat_tipo_sangre(
    cve_tipo_sangre TINYINT PRIMARY KEY,
    descripcion VARCHAR(5) NOT NULL
);

INSERT INTO cat_tipo_sangre(cve_tipo_sangre,descripcion) VALUES (1,"O+"),
 (2,"O-"),
 (3,"A+"),
 (4,"A-"),
 (5,"B+"),
 (6,"B-"),
 (7,"AB+"),
 (8,"AB-"),
 (9,"N/D");

SELECT * FROM cat_tipo_sangre;
