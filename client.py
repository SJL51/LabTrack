import getpass, json, socket, psutil, requests, time

SERVER_URL = "http://192.168.66:5000/report"
START_TIME = time.time()

# Load allowed users
with open("users.json", "r") as f:
    users = json.load(f)

# Detect current Windows username
detected_user = getpass.getuser()

# Auto-match to users.json keys (case-insensitive)
USER_NAME = None
for user_key in users:
    if detected_user.lower() == user_key.lower():
        USER_NAME = user_key
        break
if not USER_NAME:
    USER_NAME = "owner" if "owner" in users else "Unknown"

# PC hostname
PC_NAME = socket.gethostname()

def get_open_apps():
    apps = []
    for proc in psutil.process_iter(['name']):
        try:
            apps.append(proc.info['name'])
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return apps

def report():
    data = {
        "pc": f"{PC_NAME} ({USER_NAME})",
        "online": True,
        "apps": get_open_apps(),
        "uptime_seconds": round(time.time() - START_TIME)
    }
    try:
        response = requests.post(SERVER_URL, json=data, timeout=5)
        if response.status_code == 200:
            print(f"[SENT] Reported to server: {PC_NAME} ({USER_NAME}) | Uptime: {data['uptime_seconds']}s | Apps: {len(data['apps'])}")
        else:
            print(f"[ERROR] Server responded with status code {response.status_code}")
    except requests.RequestException as e:
        print(f"[FAILED] Could not report: {e}")

if __name__ == "__main__":
    while True:
        report()
        time.sleep(10)
