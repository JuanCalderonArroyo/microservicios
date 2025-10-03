import docker, uuid, os, re
import json, os

client = docker.from_env()
def redeploy_microservice(service_id: str, code: str, port: str):
    """
    Reconstruye un microservicio manteniendo el mismo ID y puerto.
    """
    print("ESTOY EN REDEPLOY, service_id:", service_id, "port:", port)
    folder = f"./services/{service_id}"
    os.makedirs(folder, exist_ok=True)

    # Sobrescribir app.py
    with open(f"{folder}/app.py", "w", encoding="utf-8") as f:
        f.write(code)

    # Detectar dependencias
    extra_deps = detect_dependencies(code)

    # requirements.txt
    with open(f"{folder}/requirements.txt", "w") as f:
        f.write("fastapi\nuvicorn\n")
        for dep in extra_deps:
            f.write(dep + "\n")

    # Dockerfile
    with open(f"{folder}/Dockerfile", "w") as f:
        f.write("""FROM python:3.11-slim
WORKDIR /app

# Instalar certificados SSL y utilidades básicas
RUN apt-get update && apt-get install -y ca-certificates curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
CMD ["python", "app.py"]""")

    # Reconstruir imagen
    image, _ = client.images.build(path=folder, tag=f"{service_id}")

    # Si ya existía un contenedor viejo con el mismo nombre, lo borramos
    try:
        old = client.containers.get(f"{service_id}")
        old.stop()
        old.remove()
    except:
        pass

    # Volver a levantar en el mismo puerto
    try:
        container = client.containers.run(
            image.id,
            detach=True,
            ports={"8000/tcp": port},
            name=f"{service_id}"
        )
    except Exception as e:
        print(f"[ERROR] No se pudo recrear el contenedor {service_id}: {e}")
        return None

    print(f"[INFO] Dependencias detectadas: {extra_deps}")
    return {"name (full)": service_id, "port": port, "status": "running"}
def get_free_port(start=5000, end=6000):
    used = set()
    for c in client.containers.list(all=True):
        ports = c.attrs["NetworkSettings"]["Ports"]
        if ports and "8000/tcp" in ports and ports["8000/tcp"]:
            used.add(int(ports["8000/tcp"][0]["HostPort"]))
    # Buscar el primer puerto libre
    for p in range(start, end):
        if p not in used:
            return str(p)
    raise RuntimeError("No hay puertos libres en el rango")

def detect_dependencies(code: str):
    import re
    pattern = r'^\s*(?:from|import)\s+([a-zA-Z0-9_]+)'
    matches = re.findall(pattern, code, flags=re.MULTILINE)

    std_libs = {
        "os", "sys", "re", "math", "json", "uuid", "datetime",
        "subprocess", "typing", "time", "pathlib"
    }

    # Diccionario de equivalencias: import -> paquete PyPI
    EQUIVALENCIAS = {
        "cv2": "opencv-python",
        "PIL": "Pillow",
        "yaml": "PyYAML",
        "Crypto": "pycryptodome",
        "sklearn": "scikit-learn",
        "bs4": "beautifulsoup4",
        "mpl_toolkits": "matplotlib",
        "gi": "PyGObject",
        "wx": "wxPython",
        "OpenGL": "PyOpenGL",
        "win32api": "pywin32",
        "win32com": "pywin32",
        "serial": "pyserial",
        "pandas_datareader": "pandas-datareader",
        "dateutil": "python-dateutil",
        "jwt": "PyJWT",
        "dotenv": "python-dotenv",
        "Levenshtein": "python-Levenshtein",
    }

    deps = []
    for m in matches:
        if m not in std_libs:
            # Usa equivalencia si existe, si no, el mismo nombre
            deps.append(EQUIVALENCIAS.get(m, m))

    return list(set(deps))  # eliminamos duplicados


def deploy_microservice(code: str, nombre: str):
    service_id = str(uuid.uuid4())[:8]
    folder = f"./services/ms-{service_id}-{nombre}"
    #folder = f"./services/{nombre}"
    os.makedirs(folder, exist_ok=True)

    with open(f"{folder}/app.py", "w", encoding="utf-8") as f:
        f.write(code)

    extra_deps = detect_dependencies(code)

    with open(f"{folder}/requirements.txt", "w") as f:
        f.write("fastapi\nuvicorn\n")
        for dep in extra_deps:
            f.write(dep + "\n")

    with open(f"{folder}/Dockerfile", "w") as f:
        f.write("""FROM python:3.11-slim
WORKDIR /app

# Instalar certificados SSL y utilidades básicas
RUN apt-get update && apt-get install -y ca-certificates curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
CMD ["python", "app.py"]""")

    #image, _ = client.images.build(path=folder, tag=f"ms-{service_id}")
    image, _ = client.images.build(path=folder, tag=f"ms-{service_id}-{nombre}")

    port = get_free_port()

    try:
        container = client.containers.run(
            image.id,
            detach=True,
            ports={"8000/tcp": port},
            #name=f"ms-{service_id}"
            name=f"ms-{service_id}-{nombre}"
        )
    except Exception as e:
        print(f"[ERROR] No se pudo crear el contenedor: {e}")
        return None

    print(f"[INFO] Dependencias detectadas: {extra_deps}")
    #return {"id": service_id, "port": port, "status": "running"}
    return {"id": service_id, "name": f"ms-{service_id}-{nombre}", "port": port, "status": "running"}

FILE = "microservices.json"

def _load_data():
    if not os.path.exists(FILE):
        return {}
    with open(FILE, "r") as f:
        try:
            return json.load(f)
        except:
            return {}

def list_microservices():
    """
    Lista todos los contenedores que tienen nombre ms-...
    """
    containers = client.containers.list(all=True)
    services = []
    for c in containers:
        if c.name.startswith("ms-"):
            data = _load_data()
            nombre=c.name.split("-")
            print("c.name: ",c.name)
            codigo = data.get(c.name, None)
            patron = r'@app\.route\(["\'](.*?)["\']'
            endpoints = re.findall(patron, codigo["code"])
            services.append({
                "id": nombre[1],
                "name": c.name,
                "nombre": nombre[2],
                "status": c.status,
                "ports": c.attrs["NetworkSettings"]["Ports"],
                "puerto": f"{c.attrs['NetworkSettings']['Ports']['8000/tcp'][0]['HostPort']}" if c.attrs["NetworkSettings"]["Ports"] and c.attrs["NetworkSettings"]["Ports"].get("8000/tcp") else "N/A",
                "url base":f"http://localhost:{c.attrs['NetworkSettings']['Ports']['8000/tcp'][0]['HostPort']}" if c.attrs["NetworkSettings"]["Ports"] and c.attrs["NetworkSettings"]["Ports"].get("8000/tcp") else "N/A",
                "links": [f"http://localhost:{c.attrs['NetworkSettings']['Ports']['8000/tcp'][0]['HostPort']}{ep}" for ep in endpoints] if c.attrs["NetworkSettings"]["Ports"] and c.attrs["NetworkSettings"]["Ports"].get("8000/tcp") else []
            })
    return services


def stop_microservice(service_id: str):
    """
    Detiene y elimina un microservicio por id.
    """
    name = f"{service_id}"
    try:
        container = client.containers.get(name)
        container.stop()
        container.remove()
        return {"name (full)": service_id, "status": "stopped"}
    except Exception as e:
        return {"error": str(e)}

def deploy_from_store(service_id: str, code: str, port: str):
    """
    Redeploy de un microservicio usando su service_id, código y puerto guardados en microservices.json.
    Se asegura de respetar el puerto guardado.
    """
    folder = f"./services/{service_id}"
    os.makedirs(folder, exist_ok=True)

    # Guardar el código en app.py
    with open(f"{folder}/app.py", "w", encoding="utf-8") as f:
        f.write(code)

    # Detectar dependencias
    extra_deps = detect_dependencies(code)

    # Crear requirements.txt
    with open(f"{folder}/requirements.txt", "w") as f:
        f.write("fastapi\nuvicorn\n")
        for dep in extra_deps:
            f.write(dep + "\n")

    # Dockerfile
    with open(f"{folder}/Dockerfile", "w") as f:
        f.write("""FROM python:3.11-slim
WORKDIR /app

RUN apt-get update && apt-get install -y ca-certificates curl && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
CMD ["python", "app.py"]""")

    # Reconstruir imagen
    image, _ = client.images.build(path=folder, tag=f"{service_id}")

    # Si ya existía un contenedor con ese nombre → eliminar
    try:
        old = client.containers.get(service_id)
        old.stop()
        old.remove()
    except:
        pass

    # Levantar contenedor en el puerto guardado
    try:
        container = client.containers.run(
            image.id,
            detach=True,
            ports={"8000/tcp": port},
            name=service_id
        )
    except Exception as e:
        print(f"[ERROR] No se pudo levantar {service_id} en puerto {port}: {e}")
        return None

    print(f"[INFO] {service_id} levantado en puerto {port} con dependencias: {extra_deps}")
    return {"name": service_id, "port": port, "status": "running"}
