import docker, uuid, os, re, json, shutil
from store import get_code, get_port, save_code, _save_data, _load_data

# 🐋 --- Obtener cliente Docker dinámicamente ---
def get_client():
    try:
        client = docker.from_env()
        client.ping()
        return client
    except Exception as e:
        print(f"[ERROR] No se pudo conectar con Docker: {e}")
        return None


# 🧠 --- Validar código del usuario ---
def validate_user_code(code: str):
    """
    Valida sintaxis del código ingresado por el usuario.
    Retorna (True, None) si es válido, o (False, mensaje_error) si hay error.
    """
    try:
        compile(code, "<string>", "exec")
        return True, None
    except SyntaxError as e:
        mensaje = f"[VALIDACIÓN] Error de sintaxis en la función del usuario: {e}"
        print(mensaje)
        return False, mensaje
    except Exception as e:
        mensaje = f"[VALIDACIÓN] Error inesperado al validar el código: {e}"
        print(mensaje)
        return False, mensaje

# 🧩 --- Crear app.py con el código del usuario dentro de un entorno Flask ---
def build_app_file(user_code: str) -> str:
    # Si el usuario ya define sus propias rutas Flask, no se envuelve
    if "@app.route" in user_code:
        return user_code.strip()

    # Caso contrario: se crea una app Flask básica
    return f"""from flask import Flask, jsonify
app = Flask(__name__)

# --- Código del usuario ---
{user_code.strip()}
# --------------------------

@app.route("/")
def main_route():
    return {extract_function_name(user_code)}()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
"""


# 🔎 --- Extraer nombre de la primera función definida ---
def extract_function_name(code: str) -> str:
    match = re.search(r'def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(', code)
    return match.group(1) if match else "main"


# 📜 --- Ver logs de un microservicio ---
def ver_logs(service_id, tail=50):
    client = get_client()
    if not client:
        print("[ERROR LOGS] Docker no disponible.")
        return
    try:
        container = client.containers.get(service_id)
        logs = container.logs(tail=tail).decode("utf-8")
        print(f"\n=== LOGS de {service_id} (últimos {tail}) ===\n{logs}")
    except docker.errors.NotFound:
        print(f"No se encontró el contenedor {service_id}.")
    except Exception as e:
        print(f"[ERROR LOGS] {e}")


# 🔁 --- Redeploy (recrear microservicio con el mismo ID y puerto) ---

# 🔁 --- Redeploy (recrear microservicio con el mismo ID y puerto) ---
def redeploy_microservice(service_id: str, code: str, port: str):
    print("ESTOY EN REDEPLOY:", service_id, "port:", port)
    client = get_client()
    if not client:
        return None

    folder = f"./services/{service_id}"
    os.makedirs(folder, exist_ok=True)

    app_code = build_app_file(code)
    with open(f"{folder}/app.py", "w", encoding="utf-8") as f:
        f.write(app_code)

    extra_deps = detect_dependencies(code)
    with open(f"{folder}/requirements.txt", "w") as f:
        f.write("fastapi\nuvicorn\nflask\n")
        for dep in extra_deps:
            f.write(dep + "\n")

    with open(f"{folder}/Dockerfile", "w") as f:
        f.write("""FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ca-certificates curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]""")

    # Eliminar imagen y contenedor viejos
    try:
        old = client.containers.get(service_id)
        old.stop()
        old.remove()
    except:
        pass
    try:
        old_img = client.images.get(service_id)
        client.images.remove(old_img.id, force=True)
    except:
        pass

    image, _ = client.images.build(path=folder, tag=f"{service_id}")

    try:
        container = client.containers.run(
            image.id,
            detach=True,
            ports={"8000/tcp": port},
            name=service_id,
            network="pc2_micro_net"
        )
    except Exception as e:
        print(f"[ERROR] No se pudo recrear el contenedor {service_id}: {e}")
        return None

    print(f"[INFO] Dependencias detectadas: {extra_deps}")
    return {"name (full)": service_id, "port": port, "status": "running"}


# 🔌 --- Cambiar puerto de un microservicio ---
def change_microservice_port(service_name: str, new_port: str):
    client = get_client()
    if not client:
        return {"error": "Docker no disponible."}

    try:
        new_port_int = int(new_port)
        if new_port_int < 5000 or new_port_int > 6000:
            return {"error": f"Puerto fuera de rango (5000–6000): {new_port}"}

        for c in client.containers.list(all=True):
            ports = c.attrs["NetworkSettings"]["Ports"]
            if ports and "8000/tcp" in ports and ports["8000/tcp"]:
                used = int(ports["8000/tcp"][0]["HostPort"])
                if used == new_port_int and c.name != service_name:
                    return {"error": f"Puerto {new_port} ya está en uso por {c.name}"}

        code = get_code(service_name)
        if not code:
            return {"error": f"No se encontró código para {service_name}"}

        try:
            container = client.containers.get(service_name)
            container.stop()
            container.remove()
        except:
            pass

        folder = f"./services/{service_name}"
        image, _ = client.images.build(path=folder, tag=service_name)
        client.containers.run(
            image.id, detach=True, ports={"8000/tcp": str(new_port_int)}, name=service_name,
            network="pc2_micro_net"
        )


        save_code(service_name, code, str(new_port_int))
        return {"name": service_name, "new_port": new_port_int, "status": "port changed"}
    except Exception as e:
        return {"error": str(e)}


# ✏️ --- Renombrar microservicio (manteniendo ID y puerto) ---
def rename_microservice(old_name: str, new_nombre: str):
    client = get_client()
    if not client:
        return {"error": "Docker no disponible."}

    parts = old_name.split("-")
    if len(parts) < 3:
        return {"error": "Formato de nombre inválido."}

    service_id = parts[1]
    new_name = f"ms-{service_id}-{new_nombre}"
    old_folder = f"./services/{old_name}"
    new_folder = f"./services/{new_name}"

    if os.path.exists(old_folder):
        shutil.move(old_folder, new_folder)

    try:
        container = client.containers.get(old_name)
        container.stop()
        container.remove()
    except:
        pass

    data = _load_data().get(old_name)
    if not data:
        return {"error": "No se encontró el registro en JSON."}

    code, port = data["code"], data["port"]

    image, _ = client.images.build(path=new_folder, tag=new_name)
    client.containers.run(
        image.id,
        detach=True,
        ports={"8000/tcp": port},
        name=new_name,
        network="pc2_micro_net"   # 🔥 importante: lo conecta a la red del proxy
    )


    json_data = _load_data()
    json_data[new_name] = json_data.pop(old_name)
    _save_data(json_data)

    return {"old": old_name, "new": new_name, "port": port, "status": "renamed"}


# 🧠 --- Detección automática de dependencias ---
def detect_dependencies(code: str):
    pattern = r'^\s*(?:from|import)\s+([a-zA-Z0-9_]+)'
    matches = re.findall(pattern, code, flags=re.MULTILINE)
    std_libs = {"os", "sys", "re", "math", "json", "uuid", "datetime", "typing", "time", "pathlib"}

    EQUIVALENCIAS = {
        "cv2": "opencv-python", "PIL": "Pillow", "yaml": "PyYAML",
        "Crypto": "pycryptodome", "sklearn": "scikit-learn", "bs4": "beautifulsoup4",
        "mpl_toolkits": "matplotlib", "gi": "PyGObject", "wx": "wxPython",
        "OpenGL": "PyOpenGL", "win32api": "pywin32", "serial": "pyserial",
        "pandas_datareader": "pandas-datareader", "dotenv": "python-dotenv",
    }

    deps = [EQUIVALENCIAS.get(m, m) for m in matches if m not in std_libs]
    return list(set(deps))


# 🚀 --- Desplegar nuevo microservicio ---
def deploy_microservice(code: str, nombre: str):
    client = get_client()
    if not client:
        print("[ERROR] Docker no está disponible.")
        return None

    service_id = str(uuid.uuid4())[:8]
    folder = f"./services/ms-{service_id}-{nombre}"
    os.makedirs(folder, exist_ok=True)

    app_code = build_app_file(code)
    with open(f"{folder}/app.py", "w", encoding="utf-8") as f:
        f.write(app_code)

    extra_deps = detect_dependencies(code)
    with open(f"{folder}/requirements.txt", "w") as f:
        f.write("fastapi\nuvicorn\nflask\n")
        for dep in extra_deps:
            f.write(dep + "\n")

    with open(f"{folder}/Dockerfile", "w") as f:
        f.write("""FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ca-certificates curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]""")

    image, _ = client.images.build(path=folder, tag=f"ms-{service_id}-{nombre}")
    port = get_free_port()

    try:
        client.containers.run(
            image.id,
            detach=True,
            ports={"8000/tcp": port},
            name=f"ms-{service_id}-{nombre}",
            network="pc2_micro_net"  # 🔹 conexión directa a la red del proxy
        )
    except Exception as e:
        print(f"[ERROR] No se pudo crear el contenedor: {e}")
        return None


    save_code(f"ms-{service_id}-{nombre}", code, port)
    print(f"[INFO] Dependencias detectadas: {extra_deps}")
    return {"id": service_id, "name": f"ms-{service_id}-{nombre}", "port": port, "status": "running"}


# 📋 --- Listar microservicios ---
# 📋 --- Listar microservicios (versión con proxy interno) ---
def list_microservices():
    client = get_client()
    if not client:
        print("[WARN] Docker no está disponible.")
        return []

    containers = client.containers.list(all=True)
    services = []

    for c in containers:
        if not c.name.startswith("ms-"):
            continue

        data = _load_data()
        nombre = c.name.split("-")
        codigo = data.get(c.name, None)
        patron = r'@app\.route\(["\'](.*?)["\']'
        endpoints = re.findall(patron, codigo["code"]) if codigo else []

        # 🔗 URLs a través del proxy interno
        proxy_base = f"http://localhost:8080/proxy/{c.name}"


        services.append({
            "id": nombre[1],
            "name": c.name,
            "nombre": nombre[2],
            "status": c.status,
            "puerto": (
                c.attrs.get("NetworkSettings", {})
                    .get("Ports", {})
                    .get("8000/tcp", [{}])[0]
                    .get("HostPort", "N/A")
            ),
            "url base": proxy_base,
            "links": [f"{proxy_base}{ep}" for ep in endpoints],
            "ports": c.attrs.get("NetworkSettings", {}).get("Ports", {})  # 👈 añade esto
        })

    return services

# 🛑 --- Detener microservicio ---
def stop_microservice(service_id: str):
    client = get_client()
    if not client:
        return {"error": "Docker no disponible."}
    try:
        container = client.containers.get(service_id)
        container.stop()
        container.remove()
        return {"name (full)": service_id, "status": "stopped"}
    except Exception as e:
        return {"error": str(e)}


# 🔁 --- Redeploy desde almacenamiento ---
def deploy_from_store(service_id: str, code: str, port: str):
    client = get_client()
    if not client:
        print("[ERROR] Docker no está disponible.")
        return None

    folder = f"./services/{service_id}"
    os.makedirs(folder, exist_ok=True)

    app_code = build_app_file(code)
    with open(f"{folder}/app.py", "w", encoding="utf-8") as f:
        f.write(app_code)

    extra_deps = detect_dependencies(code)
    with open(f"{folder}/requirements.txt", "w") as f:
        f.write("fastapi\nuvicorn\nflask\n")
        for dep in extra_deps:
            f.write(dep + "\n")

    with open(f"{folder}/Dockerfile", "w") as f:
        f.write("""FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y ca-certificates curl && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]""")

    # Eliminar contenedor e imagen anterior
    try:
        old = client.containers.get(service_id)
        old.stop()
        old.remove()
    except:
        pass
    try:
        old_img = client.images.get(service_id)
        client.images.remove(old_img.id, force=True)
    except:
        pass

    image, _ = client.images.build(path=folder, tag=f"{service_id}")

    try:
        client.containers.run(
            image.id, detach=True, ports={"8000/tcp": port}, name=service_id
        )
    except Exception as e:
        print(f"[ERROR] No se pudo levantar {service_id} en puerto {port}: {e}")
        return None

    print(f"[INFO] {service_id} levantado en puerto {port} con dependencias: {extra_deps}")
    return {"name": service_id, "port": port, "status": "running"}


# 🔍 --- Obtener puerto libre ---
def get_free_port(start=5000, end=6000):
    client = get_client()
    if not client:
        raise RuntimeError("Docker no disponible.")
    used = set()
    for c in client.containers.list(all=True):
        ports = c.attrs["NetworkSettings"]["Ports"]
        if ports and "8000/tcp" in ports and ports["8000/tcp"]:
            used.add(int(ports["8000/tcp"][0]["HostPort"]))
    for p in range(start, end):
        if p not in used:
            return str(p)
    raise RuntimeError("No hay puertos libres en el rango")


# 🧾 --- Mostrar estado actual ---
def show_status():
    print("=== Microservicios activos ===")
    for s in list_microservices():
        print(f"{s['name']} -> {s['url base']}")
    print("==============================")

# 🌐 --- Proxy interno para redirigir solicitudes a microservicios ---
import requests
from flask import request, jsonify, Response

def proxy_to_microservice(service_name: str, endpoint: str):
    try:
        client = get_client()
        if not client:
            print("[DEBUG] Docker no disponible")
            return jsonify({"error": "Docker no disponible"}), 500

        container = client.containers.get(service_name)
        if container.status != "running":
            print(f"[DEBUG] Contenedor {service_name} no está corriendo")
            return jsonify({"error": f"El microservicio {service_name} no está corriendo"}), 503

        port = "8000"
        endpoint = endpoint.lstrip("/")
        target_url = f"http://{service_name}:{port}/{endpoint}" if endpoint else f"http://{service_name}:{port}/"

        # 🔹 Logs de depuración
        print(f"[DEBUG] Proxy a URL: {target_url}")
        print(f"[DEBUG] Método: {request.method}")
        print(f"[DEBUG] Headers entrantes: {dict(request.headers)}")
        print(f"[DEBUG] Args: {request.args}")
        print(f"[DEBUG] Data: {request.get_data()}")
        print(f"[DEBUG] Cookies: {request.cookies}")

        headers = {k: v for k, v in request.headers.items() if k.lower() != "host"}

        resp = requests.request(
            method=request.method,
            url=target_url,
            headers=headers,
            params=request.args,
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False,
        )

        # 🔹 Más logs del response
        print(f"[DEBUG] Status code recibido: {resp.status_code}")
        print(f"[DEBUG] Response headers: {resp.headers}")
        print(f"[DEBUG] Response content: {resp.content[:500]}")  # solo primeros 500 bytes

        excluded_headers = ["content-encoding", "content-length", "transfer-encoding", "connection"]
        response_headers = [(k, v) for k, v in resp.headers.items() if k.lower() not in excluded_headers]

        return Response(resp.content, resp.status_code, response_headers)

    except docker.errors.NotFound:
        print(f"[DEBUG] Microservicio {service_name} no existe")
        return jsonify({"error": f"El microservicio {service_name} no existe"}), 404
    except Exception as e:
        print(f"[DEBUG] Error al conectar con {service_name}: {e}")
        return jsonify({"error": f"Error al conectar con {service_name}", "detalle": str(e)}), 502
