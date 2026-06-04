
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



#Catalogo de especialidades 

CREATE TABLE cat_especialidad(
    cve_especialidad TINYINT PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL
);

INSERT INTO cat_especialidad (cve_especialidad, descripcion) VALUES
(1, 'Medicina General'),
(2, 'Medicina Familiar'),
(3, 'Medicina Interna'),
(4, 'Pediatría'),
(5, 'Ginecología y Obstetricia'),
(6, 'Cirugía General'),
(7, 'Traumatología y Ortopedia'),
(8, 'Cardiología'),
(9, 'Dermatología'),
(10, 'Neurología'),
(11, 'Neurocirugía'),
(12, 'Oftalmología'),
(13, 'Otorrinolaringología'),
(14, 'Urología'),
(15, 'Nefrología'),
(16, 'Endocrinología'),
(17, 'Gastroenterología'),
(18, 'Neumología'),
(19, 'Reumatología'),
(20, 'Oncología Médica'),
(21, 'Oncología Pediátrica'),
(22, 'Radiooncología'),
(23, 'Cirugía Oncológica'),
(24, 'Hematología'),
(25, 'Hematología Oncológica'),
(26, 'Psiquiatría'),
(27, 'Psicología Clínica'),
(28, 'Anestesiología'),
(29, 'Urgencias Médicas'),
(30, 'Medicina Crítica'),
(31, 'Infectología'),
(32, 'Radiología e Imagen'),
(33, 'Medicina Física y Rehabilitación'),
(34, 'Geriatría'),
(35, 'Cirugía Pediátrica'),
(36, 'Cirugía Cardiovascular'),
(37, 'Cirugía Plástica y Reconstructiva'),
(38, 'Medicina del Trabajo'),
(39, 'Alergología e Inmunología'),
(40, 'Nutrición Clínica'),
(41, 'Odontología'),
(42, 'Patología'),
(43, 'Genética Médica'),
(44, 'Cuidados Paliativos'),
(45, 'Medicina del Dolor'),
(46, 'Otra');

SELECT*FROM cat_especialidad;
