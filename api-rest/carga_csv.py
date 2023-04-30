from wtforms import Form
from flask_wtf.file import FileField, FileAllowed, FileRequired


class File_form(Form):

    file = FileField('Escribe tu opinión...', validators=[  FileRequired(message='No se ha seleccionado ningún archivo.'),
        FileAllowed(['csv'], 'Solo se permiten archivos CSV')] )

   