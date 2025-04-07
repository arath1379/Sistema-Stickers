from services.api_client import get, post

def listar_inventario():
    return get("/inventario/")

def crear_inventario(data):
    return post("/inventario/", data)
