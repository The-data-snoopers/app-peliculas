from wtforms import Form
from wtforms import StringField, TextAreaField, DecimalField, SelectField, EmailField, SubmitField
from wtforms import validators


class Text_form(Form):
    texto = TextAreaField('Escribe tu opinión...',[ validators.InputRequired(message='Cuál es tu opinión?!.'),
    validators.length(min=50, max=900, message='Ingresa mínimo 50 caracteres y máximo 900 caracteres.')])

   