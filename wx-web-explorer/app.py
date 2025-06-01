from flask import Flask, render_template, request, send_file, jsonify
import sqlite3
import os
from datetime import datetime
import matplotlib.pyplot as plt
import io
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.wrappers import Response

app = Flask(__name__, static_url_path='/explorer/static')
DB_PATH = os.getenv("SQLITE_PATH", "/data/weather.db")

@app.route("/explorer/")
def index():
    # Get all columns from the database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA table_info(weather_history)")
    columns = [row[1] for row in c.fetchall() if row[1] != 'timestamp']
    conn.close()
    return render_template("explorer.html", columns=columns)

@app.route("/explorer/plot", methods=["POST"])
def plot():
    field = request.form.get("field")
    start = request.form.get("start")
    end = request.form.get("end")
    if not field or not start or not end:
        return "Missing parameters", 400
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"""
        SELECT timestamp, {field} FROM weather_history
        WHERE timestamp >= ? AND timestamp <= ?
        ORDER BY timestamp
    """, (start, end))
    rows = c.fetchall()
    conn.close()
    if not rows:
        return "No data for selection", 404
    times = [datetime.fromisoformat(r[0]) for r in rows]
    values = [r[1] for r in rows]
    plt.figure(figsize=(min(16, max(10, 0.012*request.args.get('width', 1000, type=int))), 6))
    plt.plot(times, values, linewidth=2)  # Removed marker='o'
    plt.title(f"{field} from {start} to {end}")
    plt.xlabel("Time")
    plt.ylabel(field)
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close()
    buf.seek(0)
    return send_file(buf, mimetype='image/png')

@app.route("/explorer/columns")
def columns():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("PRAGMA table_info(weather_history)")
    columns = [row[1] for row in c.fetchall() if row[1] != 'timestamp']
    conn.close()
    return jsonify(columns)

@app.route("/explorer/download", methods=["POST"])
def download_csv():
    field = request.form.get("field")
    start = request.form.get("start")
    end = request.form.get("end")
    if not field or not start or not end:
        return "Missing parameters", 400
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(f"""
        SELECT timestamp, {field} FROM weather_history
        WHERE timestamp >= ? AND timestamp <= ?
        ORDER BY timestamp
    """, (start, end))
    rows = c.fetchall()
    conn.close()
    if not rows:
        return "No data for selection", 404
    import csv
    import io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["timestamp", field])
    for row in rows:
        writer.writerow(row)
    output.seek(0)
    return send_file(
        io.BytesIO(output.read().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f"{field}_{start}_to_{end}.csv"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
