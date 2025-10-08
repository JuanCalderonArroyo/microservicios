from flask import Flask, request, jsonify
import requests
app = Flask(__name__)
@app.route("/")
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
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)