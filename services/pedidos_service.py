from services.api_client import get, post

def listar_pedidos():
    return get("/pedidos/")

def crear_pedido(data):
    return post("/pedidos/", data)
