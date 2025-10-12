# microservicios
Proyecto de contenedores PC2

# Descripción del Proyecto

Este proyecto consiste en el desarrollo de una plataforma dinámica de microservicios desplegada mediante tecnologías de contenedores Docker.
Su propósito es permitir que los usuarios puedan crear, leer, actualizar y eliminar (CRUD) microservicios de forma sencilla a través de una interfaz web interactiva, garantizando un entorno modular, escalable y completamente gestionable desde un único punto.

La arquitectura está diseñada para que cada microservicio sea independiente, además de que se encuentran diseñados para exponerse como un endpoint HTTP y devolver los resultados procesados en formato JSON.
De esta manera, la plataforma ofrece una estructura flexible que facilita la comunicación entre servicios y permite una integración sencilla con otros sistemas o aplicaciones externas.

* ⚙️ Funcionalidades principales

* 📦 Registrar nuevos microservicios y definir su lógica de procesamiento.

* ✏️ Editar características de los microservicios existentes.

* 🗑️ Eliminar microservicios.

* 🔍 Probar y visualizar los endpoints disponibles en tiempo real.

# Diagrama de arquitectura
![Imagen de WhatsApp 2025-10-06 a las 21 41 05_1b943792](https://github.com/user-attachments/assets/37b143c2-6844-4f62-84ac-ed7dfd5ab7e9)

# Instrucciones de uso
---

### 1. Requisitos previos

Antes de comenzar, asegúrate de tener instalado en tu equipo:

* 🐳 **Docker** (versión AMD64)
* 🐍 **Python**
* 🧑‍💻 **Visual Studio Code** (opcional)

---

### 2. 📥 Descargar el proyecto desde la web

1. Ingresa al repositorio en GitHub desde tu navegador.
2. Haz clic en el botón verde **“Code”** ubicado en la parte superior derecha.
3. Selecciona la opción **“Download ZIP”**.
4. Una vez descargado, **descomprime** el archivo ZIP en la ubicación que prefieras de tu computadora.
5. Abre la carpeta del proyecto descomprimido para continuar con la instalación.

---

### 3. 📦 Instalar dependencias

Ejecuta los siguientes comandos en la terminal para instalar las librerías necesarias:

```bash
pip install docker
pip install flask
```

---

### 4. 🚀 Ejecutar la aplicación

1. Ingresa a la carpeta del proyecto:

   ```bash
   cd ROBLE2/ROBLE2
   ```
2. Ejecuta la interfaz web:

   ```bash
   python web_ui.py
   ```
3. Si todo funciona correctamente, deberías ver un mensaje similar en la terminal:

```
 * Serving Flask app 'web_ui'
 * Debug mode: on
 WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://10.117.196.146:8080
 Press CTRL+C to quit
```

---

### 5. 🌐 Abrir la aplicación en el navegador

Una vez ejecutado el servidor, abre tu navegador y entra a la siguiente dirección:

👉 [http://10.117.196.146:8080](http://10.117.196.146:8080)

Al cargar la página, verás un **panel lateral izquierdo** con las siguientes opciones:

* 🏠 **Inicio**
* 📄 **Listado**
* ✍️ **Crear**
* ⚙️ **Editar configuración**
* 📜 **Ver logs**

La función principal de esta página es realizar operaciones **CRUD** (Crear, Leer, Actualizar, Eliminar) sobre microservicios, donde cada uno se ejecuta dentro de un contenedor Docker.

A continuación, se explica cada sección:

---

#### ✍️ 1. Crear

En esta sección podrás **crear un nuevo microservicio**.

* Se mostrará una caja de texto para ingresar el **nombre del microservicio**.
* Debajo encontrarás un **editor de código** donde debes escribir **solo la función** que quieres que tenga el microservicio.
* No es necesario escribir todo el código base: la aplicación lo genera automáticamente.

El código base “quemado” es el siguiente:

```python
from flask import Flask, request, jsonify
import requests
app = Flask(__name__)

@app.route("/")
# Aquí va la función que escribas
...

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
```

Una vez creada, la aplicación se encargará de **generar y desplegar el microservicio** dentro de un contenedor Docker.

---

#### 📄 2. Listado

Aquí se muestra un **listado de todos los microservicios creados**, junto con su estado actual.
Cada microservicio incluye tres botones con acciones diferentes:

* 👁️ **Ver** → Permite visualizar el código actual del microservicio.
* ✏️ **Editar código** → Abre un editor para modificar y actualizar el contenedor.
* 🗑️ **Eliminar** → Elimina el microservicio y su contenedor Docker correspondiente.

---

#### ⚙️ 3. Editar configuración

Aquí puedes **modificar el nombre y el puerto** de cualquier microservicio existente.

* Primero se mostrará una lista de microservicios.
* Al seleccionar uno, aparecerán dos campos:

  * Uno para cambiar el **nombre**.
  * Otro para modificar el **puerto**.
* Al guardar, la configuración se actualiza automáticamente en el sistema.

---

#### 📜 4. Ver logs

Esta sección permite consultar los **últimos 50 registros de logs** generados por cada contenedor Docker.

* Se mostrará una lista de microservicios.
* Al seleccionar uno, se mostrarán en pantalla las últimas 50 líneas de sus logs, lo que facilita la depuración y el monitoreo del comportamiento del microservicio.

---

# Ejemplos de solicitudes y respuestas esperadas:

  ## Ejemplo #1 (Hola mundo):
  
  Este es el texto que se tiene que agregar en la sección de codigo al momento de crear el microservicio:

  
    def saludar():
      return jsonify({"mensaje": "Hola mundo"})


  El microservicio generará un url así: http://localhost:5000/
  
  Al hacer click a la url, el json que se espera de respuesta seria:
  
    {"mensaje": "Hola mundo"}


  ## Ejemplo #2 (Sumar dos numeros):
  
  Este es el texto que se tiene que agregar en la sección de codigo al momento de crear el microservicio:

    def sumar():
      a = int(request.args.get("a", 0))
      b = int(request.args.get("b", 0))
      return jsonify({f"El resultado de {a} + {b} es": a + b})

  El microservicio generará un url así: http://localhost:5001/
  Al hacer click a la url tal cual y como se genera en un inicio, el json que se espera de respuesta seria:
    
    {"resultado":0}

  Para sumar cualquier par de números toca añadir a la url lo siguiente: un signo de pregunta seguido de a igual a su valor, de la misma forma con b y el símbolo & entre a y b (urlbase + ?a=3&b=4).
  Por ejemplo, http://localhost:5001/?a=3&b=4. Al hacer click a esta nueva url, el json que se espera de respuesta seria:
    
    {"resultado":7}

  ## Ejemplo #3 (Implementación con Roble):

  Este microservicio hace un getAll de una tabla que ya esté creada en Roble.

  Este es el texto que se tiene que agregar en la sección de codigo al momento de crear el microservicio:

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

  El microservicio generará un url así: http://localhost:5000/

  Al ingresar al link se mostrarán tres cajas de texto donde se deberán llenar con el access token, el nombre del proyecto (Ej. probando_49357d021e) y el nombre de la tabla.

  <img width="671" height="703" alt="image" src="https://github.com/user-attachments/assets/e82b947c-74ab-4ea7-aef0-3117622fb085" />

  Una vez ingresado los valores solamente hay que oprimir el botón Consultar y abajo se mostrará el json que contiene la información de la tabla a la cual se le hace el getAll.

  Se puede probar este microservicio de la siguiente manera:

  Primero seria crear otro microservicio que contenga el siguiente codigo:
  
    def main():
       res1 = requests.post("https://roble-api.openlab.uninorte.edu.co/auth/probando_49357d021e/login", json={
           "email": "yop@gmail.com",
           "password": "Asdf1234@"
       })
       return jsonify(res1.json())

  ¿Por qué se crea este microservicio? Se crea para poder obtener el accessToken de la cuenta que se creó para mostrar el ejemplo.
  
  Una vez creado el microservicio, hay que ingresar a su respectivo link y se mostrará lo siguiente:

  <img width="1919" height="243" alt="image" src="https://github.com/user-attachments/assets/c4e8981d-27fa-46a1-839a-bf0dfb20dae3" />

  Del json que se obtiene hay que copiar el accessToken (Ej. eyJhbGciOiJIUzI1NiIsInR5cCI6I...BOfwAmiuPeIzYrvz6eJimySw8FEuGHtYQA). Una vez copiado el accessToken se coloca en la primera caja de texto del microservicio que que creamos en un inicio. Despues en la segunda caja de texto se coloca: probando_49357d021e. Y en la ultima caja se pone tablita o conte que son dos tablas que ya estan creadas y tienen contenidos en ellas. Se oprime el botón Consultar y aqui está como se deberia ver una vez se haya oprimido el botón:

  <img width="671" height="866" alt="image" src="https://github.com/user-attachments/assets/02068d04-1721-4715-ac19-617bb156518e" />


  ## Ejemplo #4 (Implementación con Roble):
  
  Este microservicio hace un getAll de una tabla que ya esté creada en Roble.

  Este es el texto que se tiene que agregar en la sección de codigo al momento de crear el microservicio:
    
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

  El microservicio generará un url así: http://localhost:5000/
  
  Al hacer click a la url, mostrará una pagina sencilla con 4 cajas de textos que son donde el usuario deberá ingresar, el correo de la cuenta, la contraseña, el nombre del proyecto (Ej. probando_49357d021e) y el nombre de la tabla a la cual se le quiera hacer la lectura.

  <img width="545" height="536" alt="image" src="https://github.com/user-attachments/assets/f2f1a141-a121-44cc-a4ba-975abc2bc46a" />

  
  Para este ejemplo se deben ingresar los siguientes valores:
  
  Correo: yop@gmail.com
  
  Contraseña: Asdf1234@
  
  ID proyecto: probando_49357d021e
  
  Nombre tabla: tablita
  
  Una vez ingresado estos valores se debe oprimir el botón azul que dice Enviar y abajo se mostrará el siguiente json:

  [
  {
    "_id": "cT4ibrIo65eh",
    "edad": 20,
    "nombre": "Ana"
  },
  {
    "_id": "W5vwCvpWuvd-",
    "edad": 19,
    "nombre": "Vic"
  },
  {
    "_id": "V8brCgeC0sIb",
    "edad": 20,
    "nombre": "Gaby"
  }
]

Como se puede evidenciar el json que se obtuvo muestra la información de la tabla que se tiene en roble en el proyecto y tabla que se especificó:

<img width="1541" height="449" alt="image" src="https://github.com/user-attachments/assets/911e5803-837d-4829-9598-cc13e55d9b8f" />

Tambien se puede probar poniendo en el cmapo Nombre de tabla: conte. Es otra tabla que está ya creada en el mismo proyecto.
