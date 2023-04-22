from flask import Flask, redirect, url_for
import os
from dotenv import load_dotenv
from flask import request, render_template, abort, redirect, url_for
import pandas as pd
import numpy as np
from joblib import load
from models import Comentario
from text_form import Text_form
from Model_prediction import Model_prediction


load_dotenv()


app = Flask(__name__)

modelo = Model_prediction()



@app.route("/inicio", methods=['GET'])
def home():

    return render_template('index.html')



@app.route("/predecir", methods=['GET', 'POST'])
def crear_prediccion_comentario():

    formulario = Text_form(request.form)
    if request.method == 'GET':
        return render_template('carga.html', formulario=formulario)
        
    if request.method == 'POST' and formulario.validate():
        texto = formulario.texto.data
        print("texto: ", texto)
       

        texto = Comentario( comentario=texto)

        df = pd.DataFrame(texto.dict(), columns=texto.dict().keys(), index=[0])
    
        result = modelo.make_predictions(df)
        #result = llamar_modelo(df)
        print("result: ", result[0])
        resultado_modelo = str(result[0])
        return render_template('carga.html', formulario=formulario, result=resultado_modelo)

    else:
      
        return render_template('carga.html', formulario=formulario)
    


@app.route("/prediccion-masiva", methods=['GET', 'POST'])
def crear_prediccion_masiva():

    formulario = Text_form(request.form)
    if request.method == 'GET':
        return render_template('carga_masiva.html', formulario=formulario)
        
    if request.method == 'POST' and formulario.validate():
        texto = formulario.texto.data
        print("texto: ", texto)
       

        texto = Comentario( comentario=texto)

        df = pd.DataFrame(texto.dict(), columns=texto.dict().keys(), index=[0])
    
        result = modelo.make_predictions(df)
        #result = llamar_modelo(df)
        print("result: ", result[0])
        resultado_modelo = str(result[0])
        return render_template('carga_masiva.html', formulario=formulario, result=resultado_modelo)

    else:
      
        return render_template('carga_masiva.html', formulario=formulario)
    



@app.route('/')
def principal():
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)



