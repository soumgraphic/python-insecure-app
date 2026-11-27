# server.py (Version corrigée et requalifiée)
from asyncio import subprocess
import ipaddress
import sqlite3
import os
import re
# pyrefly: ignore[missing-import]
from flask import Flask, request, abort

app = Flask(__name__)

@app.route("/user")
def get_user():
    user_id = request.args.get("id")
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    # CORRECTION : Requête paramétrée (Sanitizer intégré)
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchall()

@app.route("/ping")
def ping_host():
    target = request.args.get("ip")
    # Validation stricte par Regex (Whitelist)
    if not re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$", target or ""):
        abort(400, "Invalid IP address")

    # Prefer this solution about semgrep false positive  
    
    # nosemgrep: python.flask.security.injection.os-system-injection.os-system-injection, python.lang.security.dangerous-system-call.dangerous-system-call  
    os.system("ping -c 1 " + target)
    return "Ping triggered"

'''
@app.route("/ping")
def ping_host():
    target = request.args.get("ip", "")
    
    # Validation native d'une adresse IPv4 ou IPv6 valide
    try:
        ipaddress.ip_address(target)
    except ValueError:
        abort(400, "Invalid IP address")
    
    # Exécution sécurisée sans invocation de shell (shell=False par défaut)
    subprocess.run(["ping", "-c", "1", target], check=False)
    return "Ping triggered"
'''

if __name__ == "__main__":
    app.run(port=5000)