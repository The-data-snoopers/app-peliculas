from flask import Flask, redirect, url_forrender_template, request, session, flash
import os
from dotenv import load_dotenv
from flask import request, render_template, abort, redirect, url_for
import pandas as pd
import numpy as np
from joblib import load
from models import Comentario
from text_form import Text_form
from Model_prediction import Model_prediction
from werkzeug.security import generate_password_hash, check_password_hash


load_dotenv()


app = Flask(__name__)

modelo = Model_prediction()

####################################
app.secret_key = os.environ.get('SECRET_KEY')

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

users = [
    User('user1', 'password1'),
    User('user2', 'password2'),
    User('user3', 'password3')
]

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = next((u for u in users if u.username == username), None)
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

#########################################


@app.route("/predecir", methods=['GET', 'POST'])
@login_required
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
@login_required
def principal():
    return redirect(url_for('prediccion.crear_prediccion'))



if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
