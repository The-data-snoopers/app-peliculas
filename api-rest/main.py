from flask import Flask, redirect, url_for
import os
from dotenv import load_dotenv
from flask import request, render_template, abort, redirect, url_for
import pandas as pd
import numpy as np
from joblib import load
from models import Comentario, User, User1
from text_form import Text_form
from Model_prediction import Model_prediction
from carga_csv import File_form
from procesamiento import predecir_comentarios, porcentaje, porcentaje_por_pelicula
from db import cantidad_peliculas, comentarios_negativos_ascedentemente, comentarios_negativos_descentemente, comentarios_positivos_ascedentemente, comentarios_positivos_descentemente, comentarios_positivos_negativos, carga_usuario, usuario_by_credential, insertar_usuario
from flask_login import LoginManager, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from user_form import Formulario_Usuario

load_dotenv()


app = Flask(__name__)
app.config['SECRET_KEY']= os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)

modelo = Model_prediction()

@login_manager.user_loader
def load_user(user_id):
    return carga_usuario(user_id)



@app.route('/registrar', methods=['GET','POST'])
def registro():

    formulario_re = Formulario_Usuario(request.form)
    if request.method == 'GET':
        return render_template('register.html', formulario=formulario_re)
        

    if request.method == 'POST' and formulario_re.validate():
        username = formulario_re.username.data
        password = formulario_re.password.data

        hashed_password = generate_password_hash(password, method='sha256')

        usuario_buscado =  usuario_by_credential(username)
        print("usuario_buscado", usuario_buscado)
        if usuario_buscado == 0:
            instancia_usuario = User1(username=username,password= hashed_password)
            usuario_insertada = insertar_usuario(instancia_usuario)
            if usuario_insertada == 0:
                return render_template('inicio_sesion.html', formulario=formulario_re)  #respuesta 
            else:
                return render_template('register.html', formulario=formulario_re, result="Opps ocurrio un error")
        else:
            return render_template('register.html', formulario=formulario_re, result="Usuario o contraseña inválida")

    else:
        return render_template('register.html', formulario=formulario_re)



@app.route('/auth', methods=['GET', 'POST'])
def inicio_sesion():

    formulario = Formulario_Usuario(request.form)
    if request.method == 'GET':
        return render_template('inicio_sesion.html', formulario=formulario)
    
    if request.method == 'POST' and formulario.validate():
        username = formulario.username.data
        password = formulario.password.data
        remember = True
        usuario_buscado =  usuario_by_credential(username)
        print("usuario_buscado", usuario_buscado)
        if usuario_buscado and check_password_hash(usuario_buscado.password, password):
            login_user(usuario_buscado, remember=remember)
            return redirect(url_for('home'))
        else:
            return render_template('inicio_sesion.html', formulario=formulario, result="Opps revisa tus credenciales o ve a registrarte")

    return render_template('inicio_sesion.html', formulario=formulario)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('principal'))



@app.route("/predecir", methods=['GET', 'POST'])
@login_required
def crear_prediccion_comentario():

    formulario = Text_form(request.form)
    if request.method == 'GET':
        return render_template('carga.html', formulario=formulario)
        
    if request.method == 'POST' and formulario.validate():
        nombres =  formulario.nombre.data
        texto = formulario.texto.data
        print("texto: ", texto)
       

        texto = Comentario(nombre=nombres, comentario=texto)

        df = pd.DataFrame(texto.dict(), columns=texto.dict().keys(), index=[0])
        print("df: ", df)
        result = modelo.make_predictions(df)
        #result = llamar_modelo(df)
        print("result: ", result[0])
        resultado_modelo = str(result[0])
        return render_template('carga.html', formulario=formulario, result=resultado_modelo)

    else:
      
        return render_template('carga.html', formulario=formulario)
    


@app.route("/prediccion-masiva", methods=['GET', 'POST'])
@login_required
def crear_prediccion_masiva():

    formulario = File_form(request.form)
    if request.method == 'GET':
        return render_template('carga_masiva.html', form=formulario)
        
    if request.method == 'POST':
        documento = request.files['file']
        print("documento:", documento)
        print("texto: ", type(documento))
        filename = documento.filename
        path = "./api-rest/assets/"+filename
        print("filename: ", filename)
        print("path: ", path)
        documento.save(path)

        resultado = predecir_comentarios(path, modelo)
        
        return redirect(url_for('estadisticas_comentarios'))

    else:
      
        return render_template('carga_masiva.html', form=formulario)
    

@app.route("/estadisticas", methods=['GET'])
@login_required
def estadisticas_comentarios():

    if request.method == 'GET':
        
        peliculas = cantidad_peliculas()
        #print("peliculas: ", peliculas)
        ne_as = comentarios_negativos_ascedentemente()
        #print("ne_as: ", ne_as)
        ne_des= comentarios_negativos_descentemente()
        #print("ne_des: ", ne_des)
        po_asc=comentarios_positivos_ascedentemente()
        #print("po_asc: ", po_asc)
        po_des= comentarios_positivos_descentemente()
        #print("po_des: ", po_des)
        po_ne= comentarios_positivos_negativos()
        #print("po_ne: ", po_ne)
        
        
        porcen= porcentaje(po_ne)
        porcentaje_pelicula = porcentaje_por_pelicula(po_ne)
        

        data_grafica = {
            "labels": [p.nombre for p in po_ne],
            "cantidad_positivos": [p.cantidad_mayor for p in po_ne],
            "cantidad_negativos": [p.cantidad_menor for p in po_ne]
            }
        

        return render_template('graficas.html', peliculas=peliculas, ne_as=ne_as, ne_des=ne_des, 
                            po_asc=po_asc, po_des=po_des, po_ne=po_ne, gra=data_grafica, total=porcen
                            , porcentaje_pelicula=porcentaje_pelicula)


@app.route('/')
def principal():
    return render_template('index.html')




@app.route("/inicio", methods=['GET'])
@login_required
def home():
    return render_template('index1.html')



@app.errorhandler(401)
def status_401(error):
    return redirect(url_for('inicio_sesion'))

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)



