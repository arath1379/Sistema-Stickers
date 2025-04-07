from services.api_client import get, post

def listar_notificaciones():
    return get("/notificaciones/")

def crear_notificacion(data):
    return post("/notificaciones/", data)
