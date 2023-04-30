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


@app.route("/predecir", methods=['GET', 'POST'])
def crear_prediccion():

    formulario = Text_form(request.form)
    if request.method == 'GET':
        return render_template('index.html', formulario=formulario)
        
    if request.method == 'POST' and formulario.validate():
        archivo = request.files['archivo']
        df = pd.read_csv(archivo)
    
        result = modelo.make_predictions(df)
        print("result: ", result[0])
        resultado_modelo = str(result[0])
        return render_template('index.html', formulario=formulario, result=resultado_modelo)

    else:
      
        return render_template('index.html', formulario=formulario)
    

@app.route('/')
def principal():
    return redirect(url_for('prediccion.crear_prediccion'))



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
