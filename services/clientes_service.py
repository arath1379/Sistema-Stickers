from services.api_client import get, post

def listar_clientes():
    return get("/clientes/")

def crear_cliente(cliente_data):
    return post("/clientes/", cliente_data)
