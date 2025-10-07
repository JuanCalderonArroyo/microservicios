# microservicios
Proyecto de contenedores PC2

Diagrama de arquitectura
![Imagen de WhatsApp 2025-10-06 a las 21 41 05_1b943792](https://github.com/user-attachments/assets/37b143c2-6844-4f62-84ac-ed7dfd5ab7e9)

Instrucciones de uso

Ejemplos de solicitudes y respuestas esperadas:

  Ejemplo #1 (Hola mundo):
  Este es el texto que se tiene que agregar en la sección de codigo al momento de crear el microservicio:
  
  def saludar():
    return jsonify({"mensaje": "Hola mundo"})

  El microservicio generará un url así: http://localhost:5000/
  Al hacer click a la url, el json que se espera de respuesta seria:
  {"mensaje": "Hola mundo"}

  Ejemplo #2 (Sumar dos numeros):
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

  Ejemplo #3 (Implementación con Roble):
  Este microservicio hace un getAll de una tabla que ya esté creada en Roble. El usuario, la contraseña, el ID del proyecto y el nombre de la tabla ya están en el codigo.
  Este es el texto que se tiene que agregar en la sección de codigo al momento de crear el microservicio:

  def main():
    res1 = requests.post("https://roble-api.openlab.uninorte.edu.co/auth/probando_49357d021e/login", json={
        "email": "yop@gmail.com",
        "password": "Asdf1234@"
    })
    user_json = res1.json()
    res = requests.get(
    "https://roble-api.openlab.uninorte.edu.co/database/probando_49357d021e/read",
    headers={"Authorization": f"Bearer {user_json.get('accessToken')}"},
    params={"tableName": "tablita"}
    )
    return jsonify(res.json())

  El microservicio generará un url así: http://localhost:5002/
  Al hacer click a la url tal cual y como se genera en un inicio, el json que se espera de respuesta seria:
  [{"_id":"cT4ibrIo65eh","edad":20,"nombre":"Ana"},{"_id":"W5vwCvpWuvd-","edad":19,"nombre":"Vic"},{"_id":"V8brCgeC0sIb","edad":20,"nombre":"Gaby"}]
  
  Esta es la tabla que ya está creada en Roble:
  <img width="1540" height="439" alt="image" src="https://github.com/user-attachments/assets/2dc48d23-4b75-4f7c-8afd-33a2da8ca556" />

  Ejemplo #4 (Implementación con Roble, con paramentros):
  Este microservicio hace un getAll de una tabla que ya esté creada en Roble. En este ejemplo toca escribir en la url el usuario, la contraseña, el ID del proyecto y el nombre de la tabla.
  Este es el texto que se tiene que agregar en la sección de codigo al momento de crear el microservicio:

  def main():
    user = request.args.get("user", "")
    password = request.args.get("password", "")
    id = request.args.get("id", "")
    tabla = request.args.get("tabla", "")
    #probando_49357d021e
    res1 = requests.post(f"https://roble-api.openlab.uninorte.edu.co/auth/{id}/login", json={
        "email": user,
        "password": password
    })
    user_json = res1.json()
    res = requests.get(
    f"https://roble-api.openlab.uninorte.edu.co/database/{id}/read",
    headers={"Authorization": f"Bearer {user_json.get('accessToken')}"},
    params={"tableName": tabla}
    )
    return jsonify(res.json())

  El microservicio generará un url así: http://localhost:5003/.
  En un inicio arrojará el siguiente json por falta de los parametros necesarios:
  {"message":"Cannot GET /read?tableName=","statusCode":404}
  
  Para poder correr adecuadamente este microservicio toca añadir a la url lo siguiente: un signo de pregunta seguido de user igual al usuario de roble, el simbolo &, password igual a la contraseña de roble, el simbolo &, id igual al id del proyecto donde esté la tabla que se desee leer, simbolo &, y por ultimo tabla igual al nombre de la tabla (urlbase+?user=yop@gmail.com&password=Asdf1234@&id=probando_49357d021e&tabla=tablita).
  Luego de tener una url de este estilo, http://localhost:5003/?user=yop@gmail.com&password=Asdf1234@&id=probando_49357d021e&tabla=tablita ya se puede obtener el json esperado el cual seria en este caso:
  [{"_id":"cT4ibrIo65eh","edad":20,"nombre":"Ana"},{"_id":"W5vwCvpWuvd-","edad":19,"nombre":"Vic"},{"_id":"V8brCgeC0sIb","edad":20,"nombre":"Gaby"}]
  En efecto, el json que se obtiene trae la información de la tabla que se especificó de roble
  <img width="1531" height="439" alt="image" src="https://github.com/user-attachments/assets/ee1ee098-b395-4e19-b497-5095cbcbd931" />

  
