from typing import NamedTuple, Optional
from typing import NamedTuple, Optional
from flask_login import UserMixin

class User(UserMixin):

    def __init__(self, idUsuario, username, password) -> None:
        self.id = idUsuario
        self.username = username
        self.password = password

class User1(NamedTuple):
    username: Optional[str] = None
    password: Optional[str] = None


    
class Comentario(NamedTuple):
    nombre: Optional[str] = None
    comentario: Optional[str] = None
    sentimiento: Optional[str] = None
    

    def dict(self):
        return {
            "review_es": self.comentario
        }
    
    def columns(self):
        return ['review_es']



class Pelicula(NamedTuple):
    nombre: Optional[str] = None
    cantidad: Optional[int] = None


class Pelicula1(NamedTuple):
    nombre: Optional[str] = None
    cantidad_menor: Optional[int] = None
    cantidad_mayor: Optional[int] = None
    