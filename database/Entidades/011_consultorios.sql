#Creacion de entidad consultorios
USE his_mx; 

CREATE TABLE consultorios (
    id_consultorio INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    ubicacion VARCHAR(100),
    activo TINYINT DEFAULT 1
);