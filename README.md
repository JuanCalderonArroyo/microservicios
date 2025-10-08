# microservicios
Proyecto de contenedores PC2

# Diagrama de arquitectura
![Imagen de WhatsApp 2025-10-06 a las 21 41 05_1b943792](https://github.com/user-attachments/assets/37b143c2-6844-4f62-84ac-ed7dfd5ab7e9)

# Instrucciones de uso
---

# 🧭 Instrucciones de uso

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
   cd ROBLE2
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
      return jsonify({"resultado": a + b})

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
  
  Al hacer click a la url, mostrará una pagina sencilla con 4 cajas de textos que son donde el usuario deberá ingresar, el correo de la cuenta, la contraseña, el ID del proyecto y el nombre de la tabla a la cual se le quiera hacer la lectura.
  
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
