from flask import Flask, request, jsonify
import requests
app = Flask(__name__)
@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>Microservicio Login</title>
        <style>
            body { font-family: Arial; display: flex; flex-direction: column; align-items: center; margin-top: 50px; }
            input, button { margin: 10px; padding: 10px; width: 250px; font-size: 16px; }
            button { cursor: pointer; background-color: #007bff; color: white; border: none; border-radius: 5px; }
            button:hover { background-color: #0056b3; }
            #resultado { margin-top: 30px; width: 80%; max-width: 600px; white-space: pre-wrap; text-align: left; }
        </style>
    </head>
    <body>
        <h2>Microservicio Login + Consulta</h2>
        <input type="text" id="user" placeholder="Correo electrónico" />
        <input type="password" id="password" placeholder="Contraseña" />
        <input type="text" id="id" placeholder="ID del proyecto (ej. probando_49357d021e)" />
        <input type="text" id="tabla" placeholder="Nombre de la tabla (ej. usuarios)" />
        <button onclick="enviar()">Enviar</button>
        <div id="resultado"></div>
  
        <script>
            async function enviar() {
                const datos = {
                    user: document.getElementById("user").value,
                    password: document.getElementById("password").value,
                    id: document.getElementById("id").value,
                    tabla: document.getElementById("tabla").value
                };
  
                const res = await fetch("/procesar", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datos)
                });
  
                const data = await res.json();
                document.getElementById("resultado").textContent = JSON.stringify(data, null, 2);
            }
        </script>
    </body>
    </html>
    """
      
@app.route("/procesar", methods=["POST"])
def procesar():
    data = request.get_json()
    user = data.get("user", "")
    password = data.get("password", "")
    id = data.get("id", "")
    tabla = data.get("tabla", "")
  
    try:
        # Paso 1: login
        res1 = requests.post(
            f"https://roble-api.openlab.uninorte.edu.co/auth/{id}/login",
            json={"email": user, "password": password}
        )
        user_json = res1.json()
  
        # Paso 2: lectura de datos
        res2 = requests.get(
            f"https://roble-api.openlab.uninorte.edu.co/database/{id}/read",
            headers={"Authorization": f"Bearer {user_json.get('accessToken')}"},
            params={"tableName": tabla}
        )
  
        return jsonify(res2.json())
  
    except Exception as e:
        return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)