from services.api_client import get, post

def listar_reportes():
    return get("/reportes/")

def crear_reporte(data):
    return post("/reportes/", data)
