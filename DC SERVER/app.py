from flask import Flask, render_template, jsonify
import psutil
import platform
import time

app = Flask(__name__)

# Startzeit des Servers merken für Uptime
start_time = time.time()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def stats():
    # Uptime berechnen
    uptime_seconds = int(time.time() - start_time)
    hours, remainder = divmod(uptime_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    uptime_str = f"{hours}h {minutes}m {seconds}s"

    # Systemdaten sammeln
    data = {
        "cpu_percent": psutil.cpu_percent(interval=None),
        "ram_percent": psutil.virtual_memory().percent,
        "ram_used_gb": round(psutil.virtual_memory().used / (1024**3), 2),
        "ram_total_gb": round(psutil.virtual_memory().total / (1024**3), 2),
        "disk_percent": psutil.disk_usage('/').percent,
        "disk_used_gb": round(psutil.disk_usage('/').used / (1024**3), 2),
        "disk_total_gb": round(psutil.disk_usage('/').total / (1024**3), 2),
        "uptime": uptime_str,
        "system_name": platform.node() or "Server"
    }
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    