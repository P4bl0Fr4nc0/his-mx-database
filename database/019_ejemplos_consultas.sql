
#Consultas realizadas por cada medico

use his_mx;
SELECT 
m.id_medico as Id,
m.nombre as Nombre,
m.apellido_paterno As Apellido_Paterno,
COUNT(c.id_consulta) AS Total_consultas
FROM medicos m
JOIN consultas c ON m.id_medico = c.id_medico
GROUP BY m.id_medico
ORDER BY total_consultas DESC;


#Top 10 diagnosticos mas fecuentes
SELECT 
    ci.descripcion AS diagnostico,
    COUNT(d.id_diagnostico) AS total
FROM diagnosticos d
JOIN cat_cie10 ci ON d.cve_cie10 = ci.cve_cie10
GROUP BY d.cve_cie10
ORDER BY total DESC
LIMIT 10;


#Pacientes con citas pendientes en los próximos 7 días
SELECT 
p.nombre AS Nombre_paciente,
p.apellido_paterno AS Apellido_Paterno_paciente,
c.fecha_hora AS Fecha_cita,
m.nombre AS Medico,
m.apellido_paterno AS Apellido_Paterno 
FROM citas c
JOIN expedientes e ON c.id_expediente = e.id_expediente
JOIN pacientes p ON e.id_paciente = p.id_paciente
JOIN medicos m ON c.id_medico = m.id_medico
WHERE c.fecha_hora BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 7 DAY)
AND c.cve_estatus_cita = 1
ORDER BY c.fecha_hora ASC;


# Pacientes con mas de una consulta y su diagnostico mas reciente
WITH consultas_por_paciente AS (
SELECT 
p.id_paciente,
p.nombre,
p.apellido_paterno,
COUNT(c.id_consulta) AS total_consultas
FROM pacientes p
JOIN expedientes e ON p.id_paciente = e.id_paciente
JOIN consultas c ON e.id_expediente = c.id_expediente
GROUP BY p.id_paciente
HAVING total_consultas > 1
),
ultimo_diagnostico AS (
SELECT 
e.id_paciente,
d.cve_cie10,
ci.descripcion AS diagnostico,
c.fecha_consulta,
ROW_NUMBER() OVER (PARTITION BY e.id_paciente ORDER BY c.fecha_consulta DESC) AS rn
FROM consultas c
JOIN expedientes e ON c.id_expediente = e.id_expediente
JOIN diagnosticos d ON c.id_consulta = d.id_consulta
JOIN cat_cie10 ci ON d.cve_cie10 = ci.cve_cie10
)
SELECT 
cp.nombre AS Nombre,
cp.apellido_paterno AS Apellido_Paterno,
cp.total_consultas AS Total_de_consultas,
ud.diagnostico AS Diagnostico,
ud.fecha_consulta AS Ultima_consulta
FROM consultas_por_paciente cp
JOIN ultimo_diagnostico ud ON cp.id_paciente = ud.id_paciente
WHERE ud.rn = 1
ORDER BY cp.total_consultas DESC;

#Seleccionar nombre, sexo tipo de sangre y estado de naciomiento de los pacientes

SELECT p.nombre as nombre, p.apellido_paterno, p.apellido_materno, cs.descripcion as sexo , cts.descripcion as tipo_sangre, cte.nombre_estado as estado_nacimiento FROM pacientes p
INNER	JOIN cat_sexo cs
ON cs.cve_sexo = p.cve_sexo
INNER JOIN cat_tipo_sangre cts
ON
cts.cve_tipo_sangre = p.cve_tipo_sangre
INNER JOIN cat_estado cte
ON 
cte.cve_estado = p.cve_estado;

#Consulta para checar los medicos y la especialidad que se le asigno con faker

SELECT m.id_medico, m.nombre, m.segundo_nombre, m.cve_especialidad, ce.descripcion FROM medicos m
INNER JOIN cat_especialidad ce
ON  ce.cve_especialidad = m.cve_especialidad;


# Consulta para ver nombre, apellido, nacionalidad y especialidad del médico
SELECT m.nombre AS Nombre, m.apellido_paterno AS Apellido, cn.nombre_pais  AS Nacionalidad, ce.descripcion AS Especialidad FROM medicos m
INNER JOIN cat_nacionalidad cn
ON m.cve_nacionalidad = cn.cve_nacionalidad
INNER JOIN cat_especialidad ce 
ON m.cve_especialidad = ce.cve_especialidad;





