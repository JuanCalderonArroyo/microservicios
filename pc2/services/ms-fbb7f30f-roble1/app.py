from flask import Flask, request, jsonify
import requests
app = Flask(__name__)
@app.route("/")
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
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)