from services.api_client import get, post

def listar_productos():
    return get("/productos/")

def crear_producto(data):
    return post("/productos/", data)
