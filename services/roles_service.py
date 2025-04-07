from services.api_client import get, post

def listar_roles():
    return get("/roles/")

def crear_rol(data):
    return post("/roles/", data)
