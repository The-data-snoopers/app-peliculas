from typing import NamedTuple, Optional

class Comentario(NamedTuple):
    comentario: Optional[str] = None
    

    def dict(self):
        return {
            "review_es": self.comentario
        }
    
    def columns(self):
        return ['review_es']