import os
import json
import sqlite3
from datetime import datetime
from paho.mqtt import client as mqtt_client

# Config
MQTT_BROKER = os.getenv("MQTT_BROKER_HOST", "mqtt.local")
MQTT_PORT = int(os.getenv("MQTT_BROKER_PORT", 1883))
MQTT_USER = os.getenv("MQTT_BROKER_USER", None)
MQTT_PASSWORD = os.getenv("MQTT_BROKER_PASSWORD", None)
MQTT_TOPIC = os.getenv("MQTT_TOPIC", "weather/loop")
DB_PATH = os.getenv("SQLITE_PATH", "/data/weather.db")

# Friendly names mapping for weather fields
FRIENDLY_NAMES = {
    "timestamp": "Timestamp",
    "usUnits": "Units",
    "sensor_id": "Sensor ID",
    "rssi": "Signal Strength",
    "sensor_battery": "Sensor Battery",
    "windSpeed_mph": "Wind Speed (mph)",
    "windGust_mph": "Wind Gust (mph)",
    "outTemp_F": "Outdoor Temp (°F)",
    "outHumidity": "Outdoor Humidity (%)",
    "pressure_inHg": "Pressure (inHg)",
    "inTemp_F": "Indoor Temp (°F)",
    "outTempBatteryStatus": "Outdoor Temp Battery Status",
    "rxCheckPercent": "RX Check (%)",
    "altimeter_inHg": "Altimeter (inHg)",
    "appTemp_F": "Apparent Temp (°F)",
    "barometer_inHg": "Barometer (inHg)",
    "cloudbase_foot": "Cloud Base (ft)",
    "dewpoint_F": "Dew Point (°F)",
    "heatindex_F": "Heat Index (°F)",
    "humidex_F": "Humidex (°F)",
    "maxSolarRad_Wpm2": "Max Solar Radiation (W/m²)",
    "rainRate_inch_per_hour": "Rain Rate (in/hr)",
    "windchill_F": "Wind Chill (°F)",
    "windrun_mile": "Wind Run (mi)",
    "rain_total": "Total Rain (in)",
    "rain_in": "Rain (in)",
    "interval_minute": "Interval (min)",
    "hourRain_in": "Hourly Rain (in)",
    "rain24_in": "24h Rain (in)",
    "dayRain_in": "Daily Rain (in)"
}

# MQTT callbacks
def on_connect(client, userdata, flags, rc):
    print(f"MQTT on_connect called with rc={rc}", flush=True)
    if rc == 0:
        print(f"Connected to MQTT Broker {MQTT_BROKER}:{MQTT_PORT}", flush=True)
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic: {MQTT_TOPIC}", flush=True)
    else:
        print(f"Failed to connect to MQTT Broker, return code {rc}", flush=True)

def on_message(client, userdata, msg):
    try:
        data = json.loads(msg.payload.decode())
        # Use dateTime as timestamp (ISO format)
        timestamp = data.get('dateTime')
        try:
            dt = datetime.fromtimestamp(float(timestamp))
            timestamp_iso = dt.isoformat()
        except Exception:
            timestamp_iso = datetime.now().isoformat()
        # Ensure all columns exist
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        for key in data.keys():
            if key == 'dateTime':
                continue
            try:
                c.execute(f"ALTER TABLE weather_history ADD COLUMN {key} REAL")
            except sqlite3.OperationalError:
                pass
        # Insert row
        columns = ['timestamp'] + [k for k in data.keys() if k != 'dateTime']
        placeholders = ['?'] * len(columns)
        values = [timestamp_iso] + [data[k] for k in data.keys() if k != 'dateTime']
        sql = f"INSERT OR REPLACE INTO weather_history ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
        print(f"SQL: {sql}", flush=True)
        print(f"Values: {values}", flush=True)
        c.execute(sql, values)
        conn.commit()
        # Show the new record
        c.execute(f"SELECT * FROM weather_history WHERE timestamp = ?", (timestamp_iso,))
        row = c.fetchone()
        print(f"Inserted row: {row}", flush=True)
        conn.close()
        print(f"Inserted weather row at {timestamp_iso}", flush=True)
    except Exception as e:
        print(f"Error processing MQTT message: {e}", flush=True)

def main():
    print(f"Starting mqtt_to_db.py with broker={MQTT_BROKER}, port={MQTT_PORT}, topic={MQTT_TOPIC}, db={DB_PATH}", flush=True)
    # Ensure table exists BEFORE starting MQTT client
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS weather_history (
            timestamp TEXT PRIMARY KEY
        )
    ''')
    # Store friendly names mapping in a dedicated table
    c.execute('''
        CREATE TABLE IF NOT EXISTS field_friendly_names (
            field TEXT PRIMARY KEY,
            friendly_name TEXT NOT NULL
        )
    ''')
    for field, friendly in FRIENDLY_NAMES.items():
        c.execute('''INSERT OR REPLACE INTO field_friendly_names (field, friendly_name) VALUES (?, ?)''', (field, friendly))
    conn.commit()
    conn.close()
    # Start MQTT
    client = mqtt_client.Client()
    if MQTT_USER and MQTT_PASSWORD:
        print(f"Using MQTT username: {MQTT_USER}", flush=True)
        client.username_pw_set(MQTT_USER, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message
    print("Connecting to MQTT broker...", flush=True)
    try:
        client.connect(MQTT_BROKER, MQTT_PORT)
    except Exception as e:
        print(f"Error connecting to MQTT broker: {e}", flush=True)
        import sys
        sys.exit(1)
    print("Connected, entering loop...", flush=True)
    client.loop_forever()

if __name__ == "__main__":
    main()
