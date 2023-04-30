from dotenv import load_dotenv
import os
import psycopg2
from models import Pelicula, Pelicula1, User, User1


load_dotenv()  # Carga las variables de entorno desde el archivo .env

def get_database_connection():
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    dbname = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    
    conexion = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    
    return conexion



def crear_comentario(comentario):
    try:
        conexion = get_database_connection()
        cursor = conexion.cursor()
        cursor.execute(
            'INSERT INTO comentario(nombre, comentario, sentimiento) VALUES (%s, %s, %s)',
            (comentario.nombre, comentario.comentario, comentario.sentimiento)
        )
        conexion.commit()
        cursor.close()
        conexion.close()
        return  True
    except Exception as e:
        print(e)
        return False
    


def cantidad_peliculas():
    try:
        conexion = get_database_connection()
        cursor = conexion.cursor()
        cursor.execute( """select comentario.nombre, count(*) as cantidad 
                            from comentario 
                            group by comentario.nombre""")
        
        registros = cursor.fetchall()
        conexion.close()
        peliculas_lista = []
        for record in registros:

            pelicula = Pelicula(nombre=record[0], cantidad=record[1])    
            peliculas_lista.append(pelicula)

        return  peliculas_lista

    except Exception as e:
        print(e)
        return False
    

def comentarios_negativos_descentemente():
    try:
        conexion = get_database_connection()
        cursor = conexion.cursor()
        cursor.execute( """SELECT nombre, 
                           SUM(CASE WHEN sentimiento = 'negativo' THEN 1 ELSE 0 END) AS comentarios_negativos
                           FROM comentario
                           GROUP BY nombre
                           ORDER BY comentarios_negativos DESC
                           LIMIT 10;""" )
        
        registros = cursor.fetchall()
        conexion.close()
        peliculas_lista = []
        for record in registros:

            pelicula = Pelicula(nombre=record[0], cantidad=record[1])    
            peliculas_lista.append(pelicula)

        return  peliculas_lista

    except Exception as e:
        print(e)
        return False
    
def comentarios_negativos_ascedentemente():
    try:
        conexion = get_database_connection()
        cursor = conexion.cursor()
        cursor.execute("""SELECT nombre, 
                          SUM(CASE WHEN sentimiento = 'negativo' THEN 1 ELSE 0 END) AS comentarios_negativos
                          FROM comentario
                          GROUP BY nombre
                          ORDER BY comentarios_negativos ASC
                          LIMIT 10; """)
        
        registros = cursor.fetchall()
        conexion.close()
        peliculas_lista = []
        for record in registros:

            pelicula = Pelicula(nombre=record[0], cantidad=record[1])    
            peliculas_lista.append(pelicula)

        return  peliculas_lista

    except Exception as e:
        print(e)
        return False
    

def comentarios_positivos_descentemente():
    try:
        conexion = get_database_connection()
        cursor = conexion.cursor()
        cursor.execute(""" SELECT nombre, 
                           SUM(CASE WHEN sentimiento = 'positivo' THEN 1 ELSE 0 END) AS comentarios_positivo
                           FROM comentario
                           GROUP BY nombre
                           ORDER BY comentarios_positivo DESC
                           LIMIT 10; """)
        
        registros = cursor.fetchall()
        conexion.close()
        peliculas_lista = []
        for record in registros:

            pelicula = Pelicula(nombre=record[0], cantidad=record[1])    
            peliculas_lista.append(pelicula)

        return  peliculas_lista

    except Exception as e:
        print(e)
        return False
    

def comentarios_positivos_ascedentemente():
    try:
        conexion = get_database_connection()
        cursor = conexion.cursor()
        cursor.execute(""" SELECT nombre, 
                           SUM(CASE WHEN sentimiento = 'positivo' THEN 1 ELSE 0 END) AS comentarios_positivo
                           FROM comentario
                           GROUP BY nombre
                           ORDER BY comentarios_positivo ASC
                           LIMIT 10;""" )
        
        registros = cursor.fetchall()
        conexion.close()
        peliculas_lista = []
        for record in registros:

            pelicula = Pelicula(nombre=record[0], cantidad=record[1])    
            peliculas_lista.append(pelicula)

        return  peliculas_lista

    except Exception as e:
        print(e)
        return False
    

def comentarios_positivos_negativos():
    try:
        conexion = get_database_connection()
        cursor = conexion.cursor()
        cursor.execute("""  SELECT nombre, 
                            SUM(CASE WHEN sentimiento = 'positivo' THEN 1 ELSE 0 END) AS comentarios_positivos, 
                            SUM(CASE WHEN sentimiento = 'negativo' THEN 1 ELSE 0 END) AS comentarios_negativos
                            FROM comentario
                            GROUP BY nombre;""" )
        
        registros = cursor.fetchall()
        conexion.close()
        peliculas_lista = []
        for record in registros:

            pelicula = Pelicula1(nombre=record[0], cantidad_mayor=record[1], cantidad_menor=record[2])    
            peliculas_lista.append(pelicula)

        return  peliculas_lista

    except Exception as e:
        print(e)
        return False
    

def usuario_by_credential(username1:str):

    try:
        conexion = get_database_connection()
        sentencia =  """select usuario.* from usuario where usuario.username = %s;"""
        with conexion.cursor() as cursor:
            cursor.execute(sentencia, (username1,))
            record = cursor.fetchone()
        conexion.close()

        usuario = User(idUsuario=record[0], username=record[1], password=record[2])   
        return usuario 
    except Exception as e:
        print(e)
        return 0
    

def carga_usuario(id_user):
    try:
        conexion = get_database_connection()
        sentencia =  """select usuario.* from usuario where usuario.id = %s;"""
        with conexion.cursor() as cursor:
            cursor.execute(sentencia, id_user)
            record = cursor.fetchone()
        conexion.close()

        usuario = User(idUsuario=record[0], username=record[1], password=record[2]) 
        
        return usuario
    except Exception as e:
        return 0


def insertar_usuario(conta: User1) -> int:
    try:
        conexion = get_database_connection()
        sentencia = "INSERT INTO usuario(username, contrasena) VALUES ( %s, %s)"
        with conexion.cursor() as cursor:
            cursor.execute(sentencia,(conta.username, conta.password))
        conexion.commit()
        conexion.close()
        return 0
    except Exception as e:
        print(e)
        return -1