from flask import Flask, render_template, jsonify, send_from_directory
import sqlite3
import os

app = Flask(__name__, static_folder=None)
DB_PATH = os.environ.get('SQLITE_PATH', '/data/weather.db')
SECRETS_PATH = '/run/secrets/wx-web-frontend.secrets'

# Load NOAA Radar and port from Docker secrets
def load_frontend_secrets():
    secrets = {'NOAA_Radar': 'KMVX', 'FRONTEND_PORT': '8080'}
    try:
        with open(SECRETS_PATH) as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    secrets[k] = v
    except Exception as e:
        print(f"Could not load frontend secrets: {e}")
    return secrets

FRONTEND_SECRETS = load_frontend_secrets()
NOAA_Radar = FRONTEND_SECRETS['NOAA_Radar']
FRONTEND_PORT = int(FRONTEND_SECRETS['FRONTEND_PORT'])

def get_latest_row():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM weather_history ORDER BY timestamp DESC LIMIT 1")
    row = c.fetchone()
    if not row:
        return {}
    # Get column names
    col_names = [desc[0] for desc in c.description]
    conn.close()
    return dict(zip(col_names, row))

def get_averages(field, hours):
    from datetime import datetime, timedelta
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"""
        SELECT AVG({field}) FROM weather_history
        WHERE timestamp >= ?
    """, (cutoff,))
    avg = c.fetchone()[0]
    conn.close()
    return round(avg, 2) if avg is not None else '--'

@app.route("/")
def index():
    import sys
    print("Index route called from web_frontend/app.py", file=sys.stderr, flush=True)  # Test print statement with flush
    latest_data = get_latest_row()
    latest_timestamp = latest_data.get("timestamp", "Unknown")
    print(f"Latest timestamp: {latest_timestamp}", file=sys.stderr, flush=True)  # Debugging line with flush
    return render_template("index.html", radar_station=NOAA_Radar, latest_timestamp=latest_timestamp)

@app.route("/api/latest")
def api_latest():
    data = get_latest_row()
    def fmt(val):
        try:
            return round(float(val), 2)
        except Exception:
            return val
    return jsonify({
        "outTemp_F": fmt(data.get("outTemp_F", "--")),
        "inTemp_F": fmt(data.get("inTemp_F", "--")),
        "maxSolarRad_Wpm2": fmt(data.get("maxSolarRad_Wpm2", "--")),
        "pressure_inHg": fmt(data.get("pressure_inHg", "--")),
        "outHumidity": fmt(data.get("outHumidity", "--")),
        "windSpeed_mph": fmt(data.get("windSpeed_mph", "--")),
    })

@app.route("/api/averages")
def api_averages():
    fields = [
        ("outTemp_F", "outside_temp"),
        ("inTemp_F", "inside_temp"),
        ("maxSolarRad_Wpm2", "solar_rad"),
        ("pressure_inHg", "pressure"),
        ("outHumidity", "humidity"),
        ("windSpeed_mph", "wind"),  # Added wind speed averages
    ]
    result = {}
    for db_field, key in fields:
        result[key] = {
            "avg_1h": get_averages(db_field, 1),
            "avg_24h": get_averages(db_field, 24)
        }
    return jsonify(result)

# Serve graph images from /data/static
@app.route('/graphs/<path:filename>')
def graph_files(filename):
    return send_from_directory('/data/static', filename)

# Serve CSS and other static files from /data/static
@app.route('/css/<path:filename>')
def css_files(filename):
    return send_from_directory('/data/static', filename)

@app.route('/css/favicon.svg')
def favicon():
    return send_from_directory('/data/static', 'favicon.svg')

@app.route('/favicon.ico')
def favicon_root():
    return send_from_directory('/data/static', 'favicon.svg')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FRONTEND_PORT)
