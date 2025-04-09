import requests

API_URL = "http://localhost:5002"  # FastAPI base URL

def get(endpoint):
    response = requests.get(f"{API_URL}{endpoint}")
    return response.json()

def post(endpoint, data):
    response = requests.post(f"{API_URL}{endpoint}", json=data)
    return response.json()
