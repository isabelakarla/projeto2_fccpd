from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/users")
def users():
    data = [
        {"id": 1, "nome": "Isa", "ativo_desde": "2005"},
        {"id": 2, "nome": "Bela", "ativo_desde": "2010"},
        {"id": 3, "nome": "Karla", "ativo_desde": "2021"}
    ]
    return jsonify(data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)