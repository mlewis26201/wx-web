from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
import threading
import time
import requests

app = Flask(__name__)
app.secret_key = os.urandom(24)

DB_PATH = os.environ.get('SQLITE_PATH', '/data/weather.db')
SECRETS_PATH = '/run/secrets/wx-web-alerter.secrets'

# Load Pushover secrets from Docker secrets
def load_pushover_secrets():
    secrets = {}
    try:
        with open(SECRETS_PATH) as f:
            for line in f:
                if '=' in line:
                    k, v = line.strip().split('=', 1)
                    secrets[k] = v
    except Exception as e:
        print(f"Could not load secrets: {e}")
    return secrets

PUSHOVER = load_pushover_secrets()

# Map DB fields to friendly names
FRIENDLY_FIELDS = {
    'temperature': 'Temperature (°C)',
    'humidity': 'Humidity (%)',
    'pressure': 'Pressure (hPa)',
    'wind_speed': 'Wind Speed (m/s)',
    'wind_gust': 'Wind Gust (m/s)',
    'rain_rate': 'Rain Rate (mm/h)',
    # Add more as needed
}

# Get available fields from DB
def get_fields():
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Use weather_history instead of weather
        c.execute('PRAGMA table_info(weather_history)')
        fields = [row[1] for row in c.fetchall()]
        conn.close()
        return fields
    except Exception as e:
        print(f"Error getting fields: {e}")
        return []

# Alert watcher thread
alerts = []
def alert_watcher():
    last_id = None
    while True:
        try:
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()
            # Use weather_history instead of weather
            c.execute('SELECT rowid, * FROM weather_history ORDER BY rowid DESC LIMIT 1')
            row = c.fetchone()
            conn.close()
            if row and (last_id is None or row[0] != last_id):
                last_id = row[0]
                for alert in alerts:
                    # row[1:] skips rowid, fields[1:] matches columns
                    value = row[1:][get_fields().index(alert['field'])]
                    if alert['direction'] == 'above' and value > alert['threshold']:
                        send_pushover(alert, value)
                    elif alert['direction'] == 'below' and value < alert['threshold']:
                        send_pushover(alert, value)
            time.sleep(5)
        except Exception as e:
            print(f"Watcher error: {e}")
            time.sleep(10)

def send_pushover(alert, value):
    user_key = PUSHOVER.get('PUSHOVER_USER_KEY')
    api_token = PUSHOVER.get('PUSHOVER_API_TOKEN')
    if not user_key or not api_token:
        print("Pushover credentials missing!")
        return
    message = f"Alert: {FRIENDLY_FIELDS.get(alert['field'], alert['field'])} was {alert['direction']} {alert['threshold']} (value: {value})"
    data = {
        'token': api_token,
        'user': user_key,
        'message': message
    }
    try:
        r = requests.post('https://api.pushover.net/1/messages.json', data=data)
        if r.status_code == 200:
            print("Pushover alert sent!")
        else:
            print(f"Pushover error: {r.text}")
    except Exception as e:
        print(f"Pushover send error: {e}")

@app.route('/', methods=['GET', 'POST'])
def index():
    fields = get_fields()
    friendly_fields = [(f, FRIENDLY_FIELDS.get(f, f)) for f in fields]
    if request.method == 'POST':
        field = request.form['field']
        direction = request.form['direction']
        threshold = float(request.form['threshold'])
        alerts.append({'field': field, 'direction': direction, 'threshold': threshold})
        flash(f"Alert set: {FRIENDLY_FIELDS.get(field, field)} {direction} {threshold}")
        return redirect(url_for('index'))
    return render_template('alerter.html', fields=friendly_fields, alerts=alerts)

if __name__ == '__main__':
    threading.Thread(target=alert_watcher, daemon=True).start()
    app.run(host='0.0.0.0', port=8082)
