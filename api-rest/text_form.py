from wtforms import Form
from wtforms import StringField, TextAreaField, DecimalField, SelectField, EmailField, SubmitField
from wtforms import validators


class Text_form(Form):
    nombre = StringField('Nombre pelicula', [validators.InputRequired(message='Falta el nombre.'), 
    validators.length(min=1, max=100, message='upps! el nombre debe tener entre 1 y 100 caracteres.')])
                                             

    texto = TextAreaField('Escribe tu opinión...',[ validators.InputRequired(message='Cuál es tu opinión?!.'),
    validators.length(min=50, max=900, message='Ingresa mínimo 50 caracteres y máximo 900 caracteres.')])

   