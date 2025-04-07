from services.api_client import get, post

def listar_proveedores():
    return get("/proveedores/")

def crear_proveedor(data):
    return post("/proveedores/", data)
