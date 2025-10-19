from flask import Flask, render_template, request, redirect, url_for, flash
from manager import (
    deploy_microservice, list_microservices, stop_microservice,
    redeploy_microservice, deploy_from_store, validate_user_code,
    rename_microservice, change_microservice_port, ver_logs
)
from store import save_code, get_codes, get_code, _load_data
import docker

app = Flask(__name__)
app.secret_key = "cambia-esta-clave"


# =================== Docker Connection ===================
def check_docker_connection():
    try:
        client = docker.from_env()
        client.ping()
        return True
    except Exception:
        return False


# =================== Levantar microservicios guardados ===================
def levantar_microservicios_guardados():
    servicios_guardados = get_codes()
    if not servicios_guardados:
        return [], [], "ℹ️ No hay microservicios guardados para levantar."

    ok, fail = [], []
    for sid, data in servicios_guardados.items():
        code = data.get("code", "")
        port = data.get("port", "")
        if not code or not port:
            fail.append(sid)
            continue

        result = deploy_from_store(sid, code, port)
        if result:
            save_code(sid, code, port)
            ok.append(f"{sid} en puerto {port}")
        else:
            fail.append(sid)

    msg = ""
    if ok:
        msg += f"✅ Levantados correctamente: {', '.join(ok)}. "
    if fail:
        msg += f"⚠️ Fallaron: {', '.join(fail)}."
    return ok, fail, msg


# =================== Página principal ===================
@app.route("/")
def home():
    connected = check_docker_connection()

    # Si Docker no está encendido → mostrar pantalla de conexión
    if not connected:
        return render_template("connect.html", connected=False, levantados=False)

    # Si Docker sí está encendido
    servicios = list_microservices()
    levantados = len(servicios) > 0

    # Mostrar vista principal
    return render_template("index.html", view="home", connected=True, levantados=levantados, servicios=servicios)


# =================== Botón Conectar ===================
@app.route("/connect", methods=["POST"])
def connect():
    if not check_docker_connection():
        flash("❌ No se pudo conectar. Verifica que Docker esté ejecutándose.", "error")
        return render_template("connect.html", connected=False, levantados=False)

    flash("✅ Conectado a Docker correctamente.", "ok")
    return redirect(url_for("home"))


# =================== Botón Levantar Microservicios ===================
@app.route("/levantar", methods=["POST"])
def levantar():
    if not check_docker_connection():
        flash("❌ Docker no está disponible.", "error")
        return redirect(url_for("home"))

    ok, fail, msg = levantar_microservicios_guardados()
    flash(msg, "ok" if ok else "error")
    return redirect(url_for("home"))


# =================== Crear microservicio ===================
import re

@app.route("/create", methods=["GET", "POST"])
def create():
    if not check_docker_connection():
        flash("Docker no está disponible.", "error")
        return redirect(url_for("home"))

    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        code = request.form.get("code", "")

        # 🔒 Validar nombre: solo letras minúsculas y números, sin espacios ni caracteres especiales
        if not re.match(r'^[a-z0-9]+$', nombre):
            flash("❌ El nombre solo puede contener letras minúsculas y números, sin espacios ni caracteres especiales.", "error")
            return redirect(url_for("create"))

        sup_code = """from flask import Flask, request, jsonify\nimport requests\napp = Flask(__name__)\n@app.route("/")\n"""
        inf_code = """\nif __name__ == "__main__":\n\tapp.run(host="0.0.0.0", port=8000)"""
        code = sup_code + code + inf_code

        if not nombre or not code:
            flash("❌ Nombre y código son obligatorios.", "error")
            return redirect(url_for("create"))

        valido, error_msg = validate_user_code(code)
        print("MSG crear:", error_msg)
        if not valido:
            flash(error_msg, "error")
            return redirect(url_for("create"))

        result = deploy_microservice(code, nombre)
        if result:
            save_code(result["name"], code, result["port"])
            flash(f"✅ Microservicio '{nombre}' desplegado en el puerto {result['port']}.", "ok")
            return redirect(url_for("list_view"))

        flash("❌ Error al desplegar microservicio.", "error")

    servicios = list_microservices()
    return render_template("index.html", view="create", servicios=servicios, connected=True)

# =================== Listar microservicios ===================
@app.route("/list")
def list_view():
    if not check_docker_connection():
        flash("Docker no está disponible.", "error")
        return redirect(url_for("home"))

    servicios = list_microservices()
    guardados = get_codes()
    return render_template("index.html", view="list", servicios=servicios, guardados=guardados, connected=True)


# =================== Ver código ===================
@app.route("/view", methods=["GET"])
def view_code():
    mid = request.args.get("id", "").strip()
    nombre = request.args.get("nombre", "").strip()
    if not mid or not nombre:
        flash("Faltan parámetros.", "error")
        return redirect(url_for("list_view"))
    sid = f"ms-{mid}-{nombre}"
    code = get_code(sid)
    if not code:
        flash("No se encontró el código del microservicio.", "error")
        return redirect(url_for("list_view"))
    return render_template("index.html", view="view", sid=sid, code=code, connected=True)


# =================== Editar código ===================
@app.route("/edit", methods=["GET", "POST"])
def edit():
    mid = request.args.get("id", "").strip()
    nombre = request.args.get("nombre", "").strip()
    if not mid or not nombre:
        flash("Faltan parámetros (id y nombre).", "error")
        return redirect(url_for("list_view"))

    sid = f"ms-{mid}-{nombre}"
    if request.method == "POST":
        new_code = request.form.get("code", "")
        valido, msg = validate_user_code(new_code)
        print("MSG:", msg)
        if not valido:
            flash(msg, "error")
            return redirect(request.url)

        servicios = list_microservices()
        puerto = None
        for s in servicios:
            if s["name"] == sid and s.get("ports") and s["ports"].get("8000/tcp"):

                puerto = s["ports"]["8000/tcp"][0]["HostPort"]
                break
        if not puerto:
            data = _load_data()
            puerto = (data.get(sid, {}) or {}).get("port", "5000")

        result = redeploy_microservice(sid, new_code, str(puerto))
        if result:
            save_code(sid, new_code, str(puerto))
            flash(f"✅ {sid} actualizado en puerto {puerto}", "ok")
        else:
            flash("❌ Error al actualizar el microservicio.", "error")
        return redirect(url_for("list_view"))

    code = get_code(sid)
    return render_template("index.html", view="edit", sid=sid, code=code, connected=True)


# =================== Eliminar ===================
@app.route("/delete", methods=["POST"])
def delete():
    mid = request.form.get("id", "").strip()
    nombre = request.form.get("nombre", "").strip()
    sid = f"ms-{mid}-{nombre}"
    stop_microservice(sid)
    flash(f"🗑️ Eliminado {sid}", "ok")
    return redirect(url_for("list_view"))


# =================== Configuración ===================
@app.route("/config", methods=["GET", "POST"])
def config_view():
    servicios = list_microservices()
    sid = request.args.get("id", "").strip()
    nombre = request.args.get("nombre", "").strip()
    service_id = f"ms-{sid}-{nombre}" if sid and nombre else None
    puerto_actual = next((s["puerto"] for s in servicios if s["id"] in sid), "N/A")

    if request.method == "POST" and service_id:
        action = request.form.get("action")
        if action == "rename":
            new_name = request.form.get("new_name", "")
            result = rename_microservice(service_id, new_name)
            flash(result.get("error", f"✅ Renombrado a {new_name}"), "ok")
        elif action == "port":
            new_port = request.form.get("new_port", "")
            result = change_microservice_port(service_id, new_port)
            flash(result.get("error", f"✅ Puerto cambiado a {new_port}"), "ok")
        return redirect(url_for("config_view"))

    return render_template(
        "index.html",
        view="config",
        servicios=servicios,
        sid=service_id,
        nombre=nombre,
        puerto=puerto_actual,
        connected=True
    )


# =================== Ver logs ===================
@app.route("/logs", methods=["GET"])
def logs():
    servicios = list_microservices()
    sid = request.args.get("id", "").strip()
    nombre = request.args.get("nombre", "").strip()
    logs_output = ""
    service_id = None

    if sid and nombre:
        service_id = f"ms-{sid}-{nombre}"
        try:
            import io, contextlib
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                ver_logs(service_id)
            logs_output = buffer.getvalue().strip() or "Sin registros."
        except Exception as e:
            logs_output = f"Error al obtener logs: {e}"

    return render_template(
        "index.html",
        view="logs",
        servicios=servicios,
        sid=service_id,
        logs=logs_output,
        connected=True
    )
# =================== proxy ===================
from manager import proxy_to_microservice

@app.route("/proxy/<service_name>/<path:endpoint>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy_route(service_name, endpoint):
    return proxy_to_microservice(service_name, endpoint)

@app.route("/proxy/<service_name>", methods=["GET", "POST", "PUT", "DELETE"])
def proxy_root(service_name):
    return proxy_to_microservice(service_name, "")

# =================== MAIN ===================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=False)


