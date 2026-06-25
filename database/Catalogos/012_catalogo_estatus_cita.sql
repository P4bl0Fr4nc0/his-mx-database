#Creacion de tabla de estatus de la cita 
USE his_mx; 
CREATE TABLE cat_estatus_cita(
    cve_estatus_cita TINYINT PRIMARY KEY,
    descripcion VARCHAR(30) NOT NULL
);
INSERT INTO cat_estatus_cita VALUES
(1,'Programada'),
(2,'Confirmada'),
(3,'Atendida'),
(4,'Cancelada'),
(5,'No asistio');