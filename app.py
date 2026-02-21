from flask import Flask, request, render_template_string, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey123"

ADMIN_PASSWORD = "admin123"


def init_db():
    conn = sqlite3.connect("/tmp/users.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            ip TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()


form_html = """
<h2>Register</h2>
<form method="POST">
    <input type="text" name="name" placeholder="Name" required><br><br>
    <input type="email" name="email" placeholder="Email" required><br><br>
    <button type="submit">Register</button>
</form>
<br>
<a href="/admin">Admin login</a>
"""

login_html = """
<h2>Admin Login</h2>
<form method="POST">
    <input type="password" name="password" placeholder="Admin password" required>
    <button type="submit">Login</button>
</form>
"""


@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        forwarded_for = request.headers.get("X-Forwarded-For", request.remote_addr)
        ip = forwarded_for.split(",")[0].strip()

        conn = sqlite3.connect("/tmp/users.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, ip) VALUES (?, ?, ?)",
            (name, email, ip)
        )
        conn.commit()
        conn.close()

    return render_template_string(form_html)


@app.route("/admin", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        if request.form["password"] == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect("/users")

    return render_template_string(login_html)


@app.route("/users")
def users():
    if not session.get("admin"):
        return "Access denied ❌"

    conn = sqlite3.connect("/tmp/users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, ip FROM users")
    all_users = cursor.fetchall()
    conn.close()

    html = "<h2>Registered Users</h2><ul>"
    for user in all_users:
        html += f"<li>{user[0]} - {user[1]} - {user[2]}</li>"
    html += "</ul><br><a href='/logout'>Logout</a>"

    return html


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
