
#Creacion de tabla de estatus registro para indicar si el paciente se encuentra Activo, Inactivo o Suspendido

CREATE TABLE cat_estatus_administrativo(
    cve_estatus_admin TINYINT PRIMARY KEY,
    descripcion VARCHAR(50) NOT NULL
);
INSERT INTO cat_estatus_administrativo VALUES
(1,'Activo'),
(2,'Inactivo'),
(3,'Suspendido'),
(4,'Dado de baja');
