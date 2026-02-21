from flask import Flask, request, redirect, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey123"

ADMIN_PASSWORD = "admin123"


# ---------- DATABASE ----------
def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            ip TEXT,
            created_at TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()


# ---------- REGISTER ----------
@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
    name = request.form["name"]
    email = request.form["email"]

    ip = request.headers.get("X-Forwarded-For", request.remote_addr)
        created_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, ip, created_at) VALUES (?, ?, ?, ?)",
            (name, email, ip, created_at)
        )
        conn.commit()
        conn.close()

    return """
    <html>
    <head>
        <title>Register</title>
        <style>
            body { font-family: Arial; background: #f4f4f4; text-align:center; }
            .box { background:white; padding:20px; width:300px; margin:100px auto; border-radius:10px; box-shadow:0 0 10px rgba(0,0,0,0.1); }
            input { width:90%; padding:8px; margin:5px 0; }
            button { padding:8px 15px; cursor:pointer; }
            a { text-decoration:none; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Register</h2>
            <form method="POST">
                <input type="text" name="name" placeholder="Name" required><br>
                <input type="email" name="email" placeholder="Email" required><br>
                <button type="submit">Register</button>
            </form>
            <br>
            <a href="/admin">Admin login</a>
        </div>
    </body>
    </html>
    """


# ---------- ADMIN LOGIN ----------
@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/users")

    return """
    <html>
    <head>
        <style>
            body { font-family: Arial; background:#f4f4f4; text-align:center; }
            .box { background:white; padding:20px; width:300px; margin:100px auto; border-radius:10px; }
            input { padding:8px; width:90%; }
            button { padding:8px 15px; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2>Admin Login</h2>
            <form method="POST">
                <input type="password" name="password" placeholder="Admin password" required><br><br>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
    </html>
    """


# ---------- USERS ----------
@app.route("/users")
def users():
    if not session.get("admin"):
        return "Access denied ❌"

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, ip, created_at FROM users")
    all_users = cursor.fetchall()
    conn.close()

    html = """
    <html>
    <head>
        <style>
            body { font-family: Arial; background:#f4f4f4; }
            .container { width:600px; margin:50px auto; }
            .user { background:white; padding:15px; margin-bottom:10px; border-radius:8px; box-shadow:0 0 5px rgba(0,0,0,0.1); }
            a { text-decoration:none; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Registered Users</h2>
    """

    for user in all_users:
        html += f"""
        <div class="user">
            <b>Name:</b> {user[0]}<br>
            <b>Email:</b> {user[1]}<br>
            <b>IP:</b> {user[2]}<br>
            <b>Time:</b> {user[3]}
        </div>
        """

    html += """
            <br>
            <a href="/logout">Logout</a>
        </div>
    </body>
    </html>
    """

    return html


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
