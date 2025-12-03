from flask import Flask
import requests

app = Flask(__name__)

@app.route("/")
def home():
    try:
        response = requests.get("http://service_a:5000/users")
        users = response.json()
    except:
        return "<h1>Erro: não consegui acessar o serviço A." \
        "</h1>"

    texto = "<h1>Lista de Usuários</h1><ul>"
    for u in users:
        texto += f"<li>{u['nome']} — ativo desde {u['ativo_desde']}</li>"
    texto += "</ul>"

    return texto

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
