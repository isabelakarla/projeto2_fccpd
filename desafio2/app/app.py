import sqlite3
import time
import os

DB_PATH = "/data/meubanco.db"

os.makedirs("/data", exist_ok=True)


conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mensagem TEXT
)
""")
conn.commit()

print("Tabela pronta. :)")


cursor.execute("INSERT INTO registros (mensagem) VALUES ('Dado persistido!')")
conn.commit()
print("Registro inserido no banco. :)")


cursor.execute("SELECT * FROM registros")
tudo = cursor.fetchall()

print("\n⚠️ Registros persistidos até agora:")
for item in tudo:
    print(item)

conn.close()


while True:
    time.sleep(5)
