from services.api_client import get, post

def listar_permisos():
    return get("/permisos/")

def crear_permiso(data):
    return post("/permisos/", data)
