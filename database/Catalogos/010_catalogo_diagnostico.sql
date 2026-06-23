USE his_mx; 

#Creacion del catalogo de diagnosticos CIE-10

CREATE TABLE cat_cie10 (
    cve_cie10        VARCHAR(5) PRIMARY KEY,
    descripcion      VARCHAR(255) NOT NULL,
    capitulo		 CHAR(5) NOT NULL,
    descripcion_capitulo         VARCHAR(255) NULL,  
    cve_sexo_aplica  TINYINT NULL        
);

