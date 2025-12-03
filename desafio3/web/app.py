from flask import Flask
import psycopg2
import redis
import os

app = Flask(__name__)

@app.route("/")
def index():
    try:
     
        conn = psycopg2.connect(
            dbname=os.getenv("POSTGRES_DB"),
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            host="db",  
            port=5432
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        postgres_version = cursor.fetchone()
        conn.close()

        r = redis.Redis(host="cache", port=6379)
        r.set("mensagem", "Cache funcionando!")
        mensagem_cache = r.get("mensagem").decode()

        return f"""
        <h1>Serviços Funcionando! :)</h1>
        <p><b>PostgreSQL:</b> {postgres_version}</p>
        <p><b>Redis:</b> {mensagem_cache}</p>
        """

    except Exception as e:
        return f"Erro ao conectar nos serviços: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
    