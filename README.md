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

Perfecto 🔥 ahora que tu proyecto ya corre dentro de su propio **contenedor Docker**, las instrucciones pueden simplificarse muchísimo — ya **no necesitas instalar Python ni Flask manualmente**, ni ejecutar el `web_ui.py` directamente.

Aquí tienes una versión **actualizada y profesional** de tu sección de **Instrucciones de uso**, adaptada al nuevo enfoque:

---

# Instrucciones de uso 

---

## 1. Requisitos previos

Antes de comenzar, asegúrate de tener instalado en tu equipo:

**Docker Desktop** (recomendado, versión AMD64 o ARM según tu sistema)
**Visual Studio Code** (opcional, si quieres explorar o editar el código)

---

## 2. Descargar el proyecto

1. Ingresa al repositorio en **GitHub**.
2. Haz clic en el botón verde **“Code”** (arriba a la derecha).
3. Selecciona **“Download ZIP”** y descomprime el archivo donde prefieras.
4. Abre la carpeta del proyecto descomprimido.

---

## 3. Iniciar el proyecto

1. Abre una **terminal** en la raíz del proyecto (donde está el archivo `docker-compose.yml`).

2. Ejecuta el siguiente comando para construir e iniciar el contenedor (solo la primera vez):**

```bash
 docker compose up --build -d
```
*(En ejecuciones posteriores puedes usar simplemente `docker compose up -d` para iniciarlo más rápido.)*

   Esto:

   * Construirá la imagen del contenedor si no existe.
   * Levantará el servicio principal (`roble-admin`).
   * Creará la red interna `micro_net` para conectar los microservicios.

3. Verifica que esté corriendo correctamente con:

   ```bash
   docker ps
   ```

   Si ves algo como esto, ¡todo está bien! ✅

   ```
   CONTAINER ID   IMAGE          NAME           STATUS         PORTS
   a1b2c3d4e5f6   roble-admin    roble-admin    Up 5 seconds   0.0.0.0:8080->8080/tcp
   ```

---

## 🌐 4. Acceder a la aplicación

Una vez iniciado el contenedor, abre tu navegador y entra a:

👉 [http://localhost:8080](http://localhost:8080)

Allí podrás usar la **interfaz web** 

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


  El microservicio generará un url así: http://localhost:8080/proxy/ms-b6befe33-ohayo
  
  Al hacer click a la url, el json que se espera de respuesta seria:
  
    {"mensaje": "Hola mundo"}


  ## Ejemplo #2 (Sumar dos numeros):
  
  Este es el texto que se tiene que agregar en la sección de codigo al momento de crear el microservicio:

    def sumar():
      a = int(request.args.get("a", 0))
      b = int(request.args.get("b", 0))
      return jsonify({f"El resultado de {a} + {b} es": a + b})

  El microservicio generará un url así: http://localhost:8080/proxy/ms-b4df01c0-sum
  Al hacer click a la url tal cual y como se genera en un inicio, el json que se espera de respuesta seria:
    
    {"resultado":0}

  Para sumar cualquier par de números toca añadir a la url lo siguiente: un signo de pregunta seguido de a igual a su valor, de la misma forma con b y el símbolo & entre a y b (urlbase + ?a=3&b=4).
  Por ejemplo, http://localhost:8080/proxy/ms-b4df01c0-sum?a=6&b=9. Al hacer click a esta nueva url, el json que se espera de respuesta seria:
    
    {"resultado":7}

  ## Ejemplo #3 (Implementación con Roble):

  Este microservicio hace un getAll de una tabla que ya esté creada en Roble.

  Este es el texto que se tiene que agregar en la sección de codigo al momento de crear el microservicio:

    def index():
      flask_url = request.host_url
      n_url = flask_url.split(":")
      nu_url = n_url[1].replace("//", "")
      return f"""
      <!DOCTYPE html>
      <html lang="es">
      <head>
         <meta charset="UTF-8">
         <title>Consulta a Roble</title>
         <style>
            body {{
               font-family: Arial, sans-serif;
               background-color: #f4f4f9;
               padding: 40px;
               display: flex;
               flex-direction: column;
               align-items: center;
            }}
            h1 {{ color: #333; }}
            textarea, input {{
               width: 400px;
               margin: 10px 0;
               padding: 10px;
               border: 1px solid #ccc;
               border-radius: 8px;
               font-size: 14px;
            }}
            button {{
               background-color: #007BFF;
               color: white;
               border: none;
               padding: 10px 20px;
               border-radius: 8px;
               cursor: pointer;
               font-size: 16px;
            }}
            button:hover {{ background-color: #0056b3; }}
            pre {{
               background: #eee;
               padding: 15px;
               border-radius: 8px;
               max-width: 600px;
               overflow-x: auto;
               white-space: pre-wrap;
               word-wrap: break-word;
            }}
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
         async function consultar() {{
             const service = "{nu_url}";
             const token = document.getElementById("tokenInput").value.trim();
             const id = document.getElementById("idInput").value.trim();
             const tabla = document.getElementById("tablaInput").value.trim();
             const resultado = document.getElementById("resultado");
      
             if (!service || !token || !id || !tabla) {{
                resultado.textContent = "Por favor, completa todos los campos.";
                return;
             }}
      
             resultado.textContent = "Consultando...";
      
             try {{
                  // Mandamos el token, id y tabla en el body JSON
                const res = await fetch(`/proxy/${{service}}/consultar`, {{
                   method: "POST",
                   headers: {{ "Content-Type": "application/json" }},
                   body: JSON.stringify({{ accessToken: token, id: id, tabla: tabla }})
                }});
      
                const json = await res.json();
                resultado.textContent = JSON.stringify(json, null, 2);
             }} catch (err) {{
                resultado.textContent = " Error al hacer la consulta: " + err;
             }}
       }}
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

  El microservicio generará un url así: http://localhost:8080/proxy/ms-5c9748c3-end

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
