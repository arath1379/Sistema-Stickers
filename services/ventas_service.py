from services.api_client import get, post

def listar_ventas():
    return get("/ventas/")

def crear_venta(data):
    return post("/ventas/", data)
