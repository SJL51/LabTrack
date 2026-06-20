# # LabTrack Core Prototype

A centralized, lightweight computer laboratory monitoring and maintenance system prototype. This project leverages an **Electron/HTML front-end UI capability** (designed through templates) interacting with a robust **Python Flask server infrastructure** and background **client tracking agents**.

---

## ⚙️ System Architecture

The prototype functions through two distinct software modules working over a local network environment:

```
[ Client Machine ] ---> (POST JSON Health Report) ---> [ Central Server (Flask) ]
     - psutil tracking                                     - Admin Dashboard UI
     - Uptime diagnostics                                 - User File Distribution
     - System validation                                   - Access Control Lists

```

1. **Central Monitoring Server (`server.py`)**: A Flask-driven backend processing network reports from endpoints, managing secure file sharing/distribution, tracking online clients, and handling role-based authorization (`admin` vs `user`).
2. **Endpoint Client Background Agent (`client.py`)**: A portable background agent running on laboratory workstations that gathers live hardware/software process tracking logs and syncs them to the backend server dynamically.

---

## 🛠️ Core Technical Features

* **Role-Based Access Control (RBAC):** Distinct permission tiers allowing administrators access to full network metrics and user account management, while standard users receive isolated access to system utilities.
* **Workstation Process Diagnostics:** Client agents scan live instances utilizing `psutil` to dynamically discover running applications across endpoints.
* **Automated Authentication Filtering:** Server-side synchronization strictly filters device logs against verified keys contained inside an integrated `users.json` repository.
* **Central Data Distribution System:** Inbound upload structures feature file distribution endpoints for deploying utilities to client machines.

---

## 🚀 Quick Setup & Deployment

### 1. Prerequisites & Environment Setup

Ensure Python 3.x is installed across deployment workstations. Install required dependencies through terminal interfaces:

```bash
pip install Flask Flask-Login Werkzeug psutil requests

```

### 2. Configuration & Identity Registration

The server initiates a localized file architecture securely. To add authorized user nodes, ensure a `users.json` layout maps required endpoint accounts:

```json
{
  "owner": {"password": "admin123", "role": "admin"},
  "pc_station_01": {"password": "userpass", "role": "user"}
}

```

> ⚠️ **Network Note:** Update the target variable `SERVER_URL` inside your client initialization scripts to perfectly trace your explicit Server Local IP mapping.

### 3. Running the Prototype

* **Initialize Monitoring Server Backend:**
```bash
python server.py

```


*The dashboard listener default establishes across port `5000` over local network interfaces (`0.0.0.0`).*
* **Initialize Workstation Reporting Agent:**
```bash
python client.py

```



---

## 📁 Repository Directory Structure

```text
├── server.py              # Flask Infrastructure, Web Routers, & File Pipelines
├── client.py              # Workstation Background Reporting & Process Utility
├── users.json             # Access Management & Local Accounts Registry
├── uploads/               # Shared File Distribution Repository
└── templates/             # Dashboard Management Views & Web Interfaces
    ├── login.html
    ├── admin_dashbroad.html
    └── user.html

```

---

> **Note:** This repository comprises the core working software prototype developed for an academic capstone evaluation. All logic components are deployed cleanly in order to demonstrate proof-of-concept network monitoring functions.
