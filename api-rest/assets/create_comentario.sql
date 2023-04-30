CREATE TABLE comentario(
		
	id SERIAL PRIMARY KEY,
	nombre VARCHAR(255) NOT NULL,
    comentario VARCHAR(4000) UNIQUE NOT NULL,
	sentimiento VARCHAR(50) NOT NULL
);


CREATE TABLE usuario
( 
	id SERIAL PRIMARY KEY,
	username VARCHAR(255) UNIQUE NOT NULL,
    contrasena VARCHAR(600) UNIQUE NOT NULL
);
