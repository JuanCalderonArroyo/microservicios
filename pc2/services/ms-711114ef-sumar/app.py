from flask import Flask, request, jsonify
import requests
app = Flask(__name__)
@app.route("/")
def sumar():
    a = int(request.args.get("a", 0))
    b = int(request.args.get("b", 0))
    return jsonify({"resultado": a + b})
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=8000)