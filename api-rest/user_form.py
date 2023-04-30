from wtforms import Form
from wtforms import StringField, PasswordField
from wtforms import validators


class Formulario_Usuario(Form):
    username = StringField('Username',[ validators.InputRequired(message='Ingresa un username!.'), 
    validators.length(min=1, max=50, message='No exceda el número de digitos !.')])

    password = PasswordField('Password',[ validators.InputRequired(message='Ingresa una contraseña!.'), 
    validators.length(min=8, max=16, message='La longitud minima son 8 caracteres!.')])
    
  