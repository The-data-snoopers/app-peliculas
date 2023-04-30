from Model_prediction import Model_prediction
import pandas as pd
from models import Comentario
from db import crear_comentario



def predecir_comentarios(documento, modelo: Model_prediction):
    
    
    numero_regsitros = 0
    df = pd.read_csv(documento)
    for i, value in enumerate(df['review_es']):
        print("value: ", value)
    
        texto = Comentario(comentario=value)

        df_u = pd.DataFrame(texto.dict(), columns=texto.dict().keys(), index=[0])
        #print("df: ", df)
        resul =  modelo.make_predictions(df_u)
        print("resultadooooooooooo: ", resul[0])
        df.loc[i,'sentimiento']  = resul[0]
    
        #insertar las registros en la base de datos
        
       
        inserccion  =  crear_comentario(Comentario(nombre=df.loc[i,'movie_name'], comentario=df.loc[i,'review_es'], sentimiento=df.loc[i,'sentimiento']))
        print("inserccion: ", inserccion)
        if inserccion:
            numero_regsitros += 1
   
    return numero_regsitros


def porcentaje(po_ne):

    total_positivos=0
    for p in po_ne:
        #print(p.cantidad_mayor)
        total_positivos += p.cantidad_mayor
    #print("total_positivos: ", total_positivos)


    total_negativos=0
    for p in po_ne:
        #print(p.cantidad_menor)
        total_negativos += p.cantidad_menor

    #print("total_negativos: ", total_negativos)
    
    total= total_positivos + total_negativos
    porcentaje_positivos = round((total_positivos/total)*100, 2)
    porcentaje_negativos = round((total_negativos/total)*100, 2)
    lista = [porcentaje_positivos, porcentaje_negativos]
    data_grafica = {
        "labels": ['Positivos', 'Negativos'],
        "datos": lista,
       
    }

    return data_grafica


def porcentaje_por_pelicula(po_ne):

    lista_negativos = []
    lista_positivos = []
    for p in po_ne:
        #print(p.cantidad_mayor)
        total_pelicula =  p.cantidad_mayor + p.cantidad_menor
        porcentaje_positivos = round((p.cantidad_mayor/total_pelicula)*100, 2)
        porcentaje_negativos = round((p.cantidad_menor/total_pelicula)*100, 2)
        lista_positivos.append(porcentaje_positivos)
        lista_negativos.append(porcentaje_negativos)
   
    data_grafica = {
        "labels": [p.nombre for p in po_ne],
        "positivos": lista_positivos,
        "negativos": lista_negativos,
       
    }

    return data_grafica




