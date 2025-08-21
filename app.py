import os
import time
import pymysql
from flask import Flask, jsonify

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASS = os.getenv("DB_PASS", "apppass")

app = Flask(__name__)

def get_conn(retries=10, delay=2):
    """Conecta a MySQL con reintentos simples (útil al arrancar todo con Compose)."""
    last_err = None
    for _ in range(retries):
        try:
            return pymysql.connect(
                host=DB_HOST, port=DB_PORT, user=DB_USER, password=DB_PASS,
                database=DB_NAME, charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor
            )
        except Exception as e:
            last_err = e
            time.sleep(delay)
    raise last_err

def ensure_schema_and_data():
    """Crea tabla y un registro por defecto si no existen."""
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                  id INT PRIMARY KEY,
                  content VARCHAR(255) NOT NULL
                );
            """)
            # Inserta “Hola mundo” si no existe el id=1
            cur.execute("INSERT IGNORE INTO messages (id, content) VALUES (1, 'Hola mundo');")
        conn.commit()
    finally:
        conn.close()

@app.route("/api/hello", methods=["GET"])
def hello():
    ensure_schema_and_data()
    conn = get_conn()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT content FROM messages WHERE id=1 LIMIT 1;")
            row = cur.fetchone()
            msg = row["content"] if row else "Hola mundo"
            return jsonify({"message": msg}), 200
    finally:
        conn.close()

@app.route("/health", methods=["GET"])
def health():
    try:
        conn = get_conn(retries=1, delay=0)
        conn.close()
        return jsonify({"status": "ok"}), 200
    except Exception:
        return jsonify({"status": "degraded"}), 503

if __name__ == "__main__":
    # Para desarrollo local (sin gunicorn): python app.py
    app.run(host="0.0.0.0", port=5000)
