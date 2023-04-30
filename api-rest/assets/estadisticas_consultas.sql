/*cantidad de comentarios por pelicula*/
select comentario.nombre, count(*) as cantidad
from comentario
group by comentario.nombre


/*cantidad de comentarios positivos y negativos por pelicula*/
SELECT nombre, 
       SUM(CASE WHEN sentimiento = 'positivo' THEN 1 ELSE 0 END) AS comentarios_positivos, 
       SUM(CASE WHEN sentimiento = 'negativo' THEN 1 ELSE 0 END) AS comentarios_negativos
FROM comentario
GROUP BY nombre;


/*comentarios negativos descentemente*/
SELECT nombre, 
       SUM(CASE WHEN sentimiento = 'negativo' THEN 1 ELSE 0 END) AS comentarios_negativos
FROM comentario
GROUP BY nombre
ORDER BY comentarios_negativos DESC
LIMIT 10;


/*comentarios negativos ascendemente*/
SELECT nombre, 
       SUM(CASE WHEN sentimiento = 'negativo' THEN 1 ELSE 0 END) AS comentarios_negativos
FROM comentario
GROUP BY nombre
ORDER BY comentarios_negativos ASC
LIMIT 10;


/*comentarios positivos descentemente*/
SELECT nombre, 
       SUM(CASE WHEN sentimiento = 'positivo' THEN 1 ELSE 0 END) AS comentarios_positivo
FROM comentario
GROUP BY nombre
ORDER BY comentarios_positivo DESC
LIMIT 10;


/*comentarios positivos ascendemente*/
SELECT nombre, 
       SUM(CASE WHEN sentimiento = 'positivo' THEN 1 ELSE 0 END) AS comentarios_positivo
FROM comentario
GROUP BY nombre
ORDER BY comentarios_positivo ASC
LIMIT 10;

