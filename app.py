from flask import Flask
from routes.public import home, lab_view
from routes.auth import login, logout
from routes.admin import admin_bp

app = Flask(__name__)
app.secret_key = "super_secret_key_antigravity"

# Public routes
app.add_url_rule("/", "home", home)
app.add_url_rule("/lab/<lab_id>", "lab_view", lab_view)

# Auth routes
app.add_url_rule("/login", "login", login, methods=["GET", "POST"])
app.add_url_rule("/logout", "logout", logout)

# Admin routes
app.register_blueprint(admin_bp)

if __name__ == "__main__":
    app.run(debug=True)
