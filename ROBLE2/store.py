import json, os

FILE = "microservices.json"

def _load_data():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}

def _save_data(data):
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_code(service_id, code, port):
    """Guarda o actualiza el código de un microservicio"""
    data = _load_data()
    data[service_id] = {"code": code, "port": port}
    _save_data(data)

def get_code(service_id):
    """Devuelve el código de un microservicio por su ID"""
    data = _load_data()
    service = data.get(service_id, None)
    return service["code"]

def get_port(service_id):
    """Devuelve el código de un microservicio por su ID"""
    data = _load_data()
    service = data.get(service_id, None)
    return service["port"]

def get_codes():
    """Devuelve todos los microservicios guardados"""
    return _load_data()
