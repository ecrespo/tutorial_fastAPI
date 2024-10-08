from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    nombre: str
    correo: str

class PostCreate(BaseModel):
    titulo: str
    contenido: str
    usuario_id: int