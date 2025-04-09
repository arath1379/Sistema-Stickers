# services/productos_service.py
import requests

API_BASE_URL = "http://localhost:5002"

def listar_productos():
    try:
        response = requests.get(f"{API_BASE_URL}/productos/")
        if response.status_code == 200:
            return response.json()
        else:
            print("Error al obtener productos:", response.status_code)
            return []
    except Exception as e:
        print("Excepción al obtener productos:", str(e))
        return []
