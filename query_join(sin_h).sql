CREATE TABLE resumen_datos as (
	SELECT 
    cp.distrito_id, 
    a.name, 
    a.alqtbid12_m_vc_22, 
    v.variacion_anual, 
    h.total_hospitales,
    bm.total_metro,
	COUNT(CASE WHEN c.regimen = 'PÚBLICO' THEN 1 END) AS total_colegios_publicos,
    COUNT(CASE WHEN c.regimen = 'PRIVADO' THEN 1 END) AS total_colegios_privados,
    COUNT(CASE WHEN c.regimen = 'CONCERTADO' THEN 1 END) AS total_colegios_concertados
FROM codigos_postales cp
LEFT JOIN colegios c ON cp.codigo_postal = c.codigo_postal
LEFT JOIN alquiler a ON cp.distrito_id = a.distrito_id
LEFT JOIN variacion_precio v ON a.name = v.name
LEFT JOIN distritos_id d ON cp.distrito_id = d.distrito_id
LEFT JOIN hospitales h ON d.distrito_id = h.distrito_id
LEFT JOIN (
    SELECT 
        d.distrito_id, 
        COUNT(bm.denominacion) AS total_metro
    FROM distritos_id d
    LEFT JOIN bocas_metro bm ON d.name = bm.distrito
    GROUP BY d.distrito_id
) bm ON d.distrito_id = bm.distrito_id
GROUP BY 
    cp.distrito_id, 
    a.name, 
    a.alqtbid12_m_vc_22, 
    v.variacion_anual, 
    d.name, 
    h.total_hospitales, 
    bm.total_metro
ORDER BY cp.distrito_id ASC
	);