from flask import Flask, request, jsonify
import requests
app = Flask(__name__)
@app.route("/")
def index():
   return """
   <!DOCTYPE html>
   <html lang="es">
   <head>
      <meta charset="UTF-8">
      <title>Consulta a Roble</title>
      <style>
         body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            padding: 40px;
            display: flex;
            flex-direction: column;
            align-items: center;
         }
         h1 { color: #333; }
         textarea, input {
            width: 400px;
            margin: 10px 0;
            padding: 10px;
            border: 1px solid #ccc;
            border-radius: 8px;
            font-size: 14px;
         }
         button {
            background-color: #007BFF;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
         }
         button:hover { background-color: #0056b3; }
         pre {
            background: #eee;
            padding: 15px;
            border-radius: 8px;
            max-width: 600px;
            overflow-x: auto;
            white-space: pre-wrap;
            word-wrap: break-word;
         }
      </style>
   </head>
   <body>
      <h1>Consulta a Roble</h1>
      <p>Introduce el access token, el ID del proyecto y el nombre de la tabla:</p>

      <input type="text" id="tokenInput" placeholder="Access token"><br>
      <input type="text" id="idInput" placeholder="ID del proyecto (por ejemplo: probando_49357d021e)"><br>
      <input type="text" id="tablaInput" placeholder="Nombre de la tabla"><br>

      <button onclick="consultar()">Consultar</button>

      <h3>Resultado:</h3>
      <pre id="resultado"></pre>

      <script>
      async function consultar() {
          const token = document.getElementById("tokenInput").value.trim();
          const id = document.getElementById("idInput").value.trim();
          const tabla = document.getElementById("tablaInput").value.trim();
          const resultado = document.getElementById("resultado");

          if (!token || !id || !tabla) {
              resultado.textContent = "Por favor, completa todos los campos.";
              return;
          }

          resultado.textContent = "Consultando...";

          try {
            // Mandamos el token, id y tabla en el body JSON
              const res = await fetch(`/consultar`, {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify({ accessToken: token, id: id, tabla: tabla })
              });

              const json = await res.json();
              resultado.textContent = JSON.stringify(json, null, 2);
          } catch (err) {
              resultado.textContent = "❌ Error al hacer la consulta: " + err;
          }
      }
      </script>
   </body>
   </html>
   """


@app.route("/consultar", methods=["POST"])
def consultar():
   try:
       data = request.get_json()
       access_token = data.get("accessToken", "")
       project_id = data.get("id", "")
       table_name = data.get("tabla", "")

       if not access_token or not project_id or not table_name:
           return jsonify({
               "error": "Faltan parámetros requeridos",
               "detalle": {
                   "accessToken": bool(access_token),
                   "id": bool(project_id),
                   "tabla": bool(table_name)
               }
           }), 400

       res = requests.get(
           f"https://roble-api.openlab.uninorte.edu.co/database/{project_id}/read",
           headers={"Authorization": f"Bearer {access_token}"},
           params={"tableName": table_name}
       )

       return jsonify(res.json()), res.status_code

   except Exception as e:
       return jsonify({"error": str(e)}), 500
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)