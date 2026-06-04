
USE his_mx; 

#Catalogo de sexo 
CREATE TABLE cat_sexo(
cve_sexo TINYINT PRIMARY KEY,
descripcion VARCHAR (20) NOT NULL
);

INSERT INTO cat_sexo
(cve_sexo, descripcion)
VALUES (1,'Masculino'), (2,'Femenino'), (3,'No especificado');

#Catalogo de parentesco para usar en tabla contacto de emergencia
CREATE TABLE cat_parentesco(
    cve_parentesco TINYINT PRIMARY KEY,
    descripcion VARCHAR(10) NOT NULL
); 

INSERT INTO cat_parentesco(cve_parentesco,descripcion) VALUES (1,"Padre");
INSERT INTO cat_parentesco(cve_parentesco,descripcion) VALUES (2,"Madre");
INSERT INTO cat_parentesco(cve_parentesco,descripcion) VALUES (3,"Cónyugue");
INSERT INTO cat_parentesco(cve_parentesco,descripcion) VALUES (4,"Hijo");
INSERT INTO cat_parentesco(cve_parentesco,descripcion) VALUES (5,"Hermano");
INSERT INTO cat_parentesco(cve_parentesco,descripcion) VALUES (6,"Tutor");
INSERT INTO cat_parentesco(cve_parentesco,descripcion) VALUES (7,"Amigo");
INSERT INTO cat_parentesco(cve_parentesco,descripcion) VALUES (8,"Otro");

SELECT * FROM cat_sexo;
SELECT * FROM cat_parentesco;
