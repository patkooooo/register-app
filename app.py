from flask import Flask, request, render_template_string

app = Flask(__name__)

form_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Register</title>
</head>
<body>
    <h2>Registration Form</h2>
    <form method="POST">
        <label>Name:</label><br>
        <input type="text" name="name" required><br><br>

        <label>Email:</label><br>
        <input type="email" name="email" required><br><br>

        <button type="submit">Register</button>
    </form>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        return f"<h2>Thanks {name}! You registered with {email} 🎉</h2>"

    return render_template_string(form_html)

if __name__ == "__main__":
    app.run(debug=True)
