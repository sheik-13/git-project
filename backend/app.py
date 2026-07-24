from flask import Flask, jsonify, request
import pymysql
import os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "172.16.1.9")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_NAME = os.getenv("DB_NAME", "myttier")
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "Sheik@123")


def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASS,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        ssl={"ssl": {}}
    )


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# GET ALL USERS
@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name FROM users ORDER BY id ASC")
            rows = cur.fetchall()

        return jsonify(rows)

    finally:
        conn.close()


# ADD USER
@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO users(name) VALUES (%s)",
                (data["name"],)
            )

            conn.commit()

            new_id = cur.lastrowid

        return jsonify({
            "id": new_id,
            "name": data["name"]
        }), 201

    finally:
        conn.close()


# UPDATE USER
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):

    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    conn = get_db_connection()

    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET name=%s WHERE id=%s",
                (data["name"], user_id)
            )

            conn.commit()

        return jsonify({
            "id": user_id,
            "name": data["name"]
        })

    finally:
        conn.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)