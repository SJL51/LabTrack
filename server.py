from flask import Flask, request, jsonify, render_template, send_from_directory, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os, time, json

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

USERS_FILE = "users.json"

# ---------------------- LOAD USERS ----------------------
if os.path.exists(USERS_FILE):
    with open(USERS_FILE, "r") as f:
        users = json.load(f)
else:
    users = {"owner": {"password": "admin123", "role": "admin"}}
    with open(USERS_FILE, "w") as f:
        json.dump(users, f)

# ---------------------- LOGIN SYSTEM ----------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, role):
        self.id = id
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id, users[user_id]["role"])
    return None

# ---------------------- CLIENT MONITORING ----------------------
clients = {}
admin_start_time = None
client_start_times = {}

def format_uptime(seconds):
    mins, secs = divmod(seconds, 60)
    hrs, mins = divmod(mins, 60)
    if hrs > 0:
        return f"{hrs} hr {mins} min {secs} sec"
    elif mins > 0:
        return f"{mins} min {secs} sec"
    else:
        return f"{secs} sec"

@app.route("/report", methods=["POST"])
def report():
    data = request.json
    pc = data.get("pc")

    #print(f"Received report: {data}")  # Log the incoming client report

    if pc:
        # Extract username part -> "pcname (username)"
        if "(" in pc and ")" in pc:
            reported_user = pc.split("(")[-1].split(")")[0].strip()
        else:
            reported_user = None

        # Only accept reports if user exists in users.json
        if reported_user and reported_user in users:
            uptime_seconds = data.get("uptime_seconds", 0)
            clients[pc] = {
                "online": data.get("online", False),
                "apps": data.get("apps", []),
                "uptime": format_uptime(uptime_seconds),
                "uptime_seconds": uptime_seconds,
                "user": reported_user
            }
 #           print(f"Updated clients dict: {clients}")  # Log current clients
 #       else:
 #           print(f"Ignored report from unknown user: {reported_user}")

    return "OK", 200


# ---------------------- ROUTES ----------------------
@app.route("/")
def index():
    if current_user.is_authenticated:
        if current_user.role == "admin":
            return redirect(url_for("admin_dashboard"))
        else:
            return redirect(url_for("user_dashboard"))
    return redirect(url_for("login"))

@app.route("/login", methods=["GET", "POST"])
def login():
    global admin_start_time

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username in users and users[username]["password"] == password:
            user = User(username, users[username]["role"])
            login_user(user)
            if user.role == "admin":
                admin_start_time = time.time()
            return redirect(url_for("index"))
        else:
            flash("Invalid credentials")
            
    return render_template("login.html")


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/admin")
@login_required
def admin_dashboard():
    if current_user.role != "admin":
        return "Access denied", 403

    files = os.listdir(app.config["UPLOAD_FOLDER"])
    uptime = round(time.time() - admin_start_time) if admin_start_time else 0
    admin_status = {"online": current_user.is_authenticated, "uptime": format_uptime(uptime)}

    return render_template(
        "admin_dashbroad.html",
        files=files,
        users=users,
        clients=clients,
        admin_status=admin_status
    )

@app.route("/user")
@login_required
def user_dashboard():
    files = os.listdir(app.config["UPLOAD_FOLDER"])
    return render_template("user.html", files=files)

@app.route("/status")
def get_status():
    uptime = round(time.time() - admin_start_time) if admin_start_time else 0
    status_clients = {}
    for pc, info in clients.items():
        status_clients[pc] = {
            "online": info.get("online", False),
            "apps": info.get("apps", []),
            "uptime": info.get("uptime", "0 sec"),
            "uptime_seconds": info.get("uptime_seconds", 0)
        }
    return jsonify({
        "admin": True if admin_start_time else False,
        "admin_uptime": format_uptime(uptime),
        "admin_uptime_seconds": uptime,
        "clients": status_clients
    })

# ---------------------- FILE HANDLING ----------------------
@app.route("/upload", methods=["POST"])
@login_required
def upload():
    print(f"UPLOAD by {current_user.id} with role {current_user.role}")  # <-- Debug
    
    if "file" not in request.files:
        return "No file part"
    file = request.files["file"]
    if file.filename == "":
        return "No selected file"
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    if current_user.role == "admin":
        return redirect(url_for("admin_dashboard"))
    else:
        return redirect(url_for("user_dashboard"))



@app.route("/download/<filename>")
@login_required
def download(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

# ---------------------- USER MANAGEMENT ----------------------
@app.route("/add_user", methods=["POST"])
@login_required
def add_user():
    if current_user.role != "admin":
        return "Access denied", 403
    username = request.form["username"]
    password = request.form["password"]
    role = request.form["role"]
    if username in users:
        flash("User already exists")
    else:
        users[username] = {"password": password, "role": role}
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)
    return redirect(url_for("admin_dashboard"))

@app.route("/delete_user/<username>")
@login_required
def delete_user(username):
    if current_user.role != "admin":
        return "Access denied", 403
    if username in users and username != "owner":
        del users[username]
        with open(USERS_FILE, "w") as f:
            json.dump(users, f)
    return redirect(url_for("admin_dashboard"))

# ---------------------- RUN SERVER ----------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
