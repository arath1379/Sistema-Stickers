from services.api_client import get, post

def listar_usuarios():
    return get("/usuarios/")

def crear_usuario(data):
    return post("/usuarios/", data)
