import os
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import matplotlib.dates as mdates
import time
import numpy as np

DB_PATH = os.getenv("SQLITE_PATH", "/data/weather.db")
STATIC_DIR = os.getenv("STATIC_DIR", "/data/static/graphs")

os.makedirs(STATIC_DIR, exist_ok=True)

# --- Temperature Graphs ---
def fetch_temp_data(hours):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    c.execute(f"""
        SELECT timestamp, outTemp_F, inTemp_F FROM weather_history
        WHERE timestamp >= ?
        ORDER BY timestamp
    """, (cutoff,))
    rows = c.fetchall()
    conn.close()
    times, out_temps, in_temps = [], [], []
    for t, out_t, in_t in rows:
        try:
            times.append(datetime.fromisoformat(t))
            out_temps.append(float(out_t) if out_t is not None else None)
            in_temps.append(float(in_t) if in_t is not None else None)
        except Exception:
            continue
    return times, out_temps, in_temps

def plot_temp_graph(hours):
    times, out_temps, in_temps = fetch_temp_data(hours)
    if not times:
        print(f"No temperature data for last {hours} hours.")
        return
    plt.figure(figsize=(10,5), facecolor='#222831')
    ax = plt.gca()
    ax.set_facecolor('#222831')
    plt.plot(times, out_temps, label="Outdoor Temp (°F)", color="#00b4d8", linewidth=1)
    plt.plot(times, in_temps, label="Indoor Temp (°F)", color="#28a745", linewidth=1)
    plt.title(f"Indoor & Outdoor Temperature - Last {hours} Hour(s)", color='white', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Time", color='white', fontsize=13, fontweight='bold')
    plt.ylabel("Temperature (°F)", color='white', fontsize=13, fontweight='bold')
    plt.legend(facecolor='#222831', frameon=False, fontsize=12, loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=2)
    plt.grid(True, linestyle='--', alpha=0.5, color='#393e46')
    if hours <= 24:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %I:%M %p'))
    plt.gcf().autofmt_xdate()
    ax.tick_params(colors='white', labelsize=11)
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.title.set_color('white')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color('white')
    plt.tight_layout(rect=[0,0.08,1,1])
    img_path = os.path.join(STATIC_DIR, f"temp_line_{hours}h.png")
    plt.savefig(img_path, facecolor='#222831')
    plt.close()
    print(f"Saved {img_path}")

# --- Humidity Graphs ---
def fetch_humidity_data(hours):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    c.execute(f"""
        SELECT timestamp, outHumidity FROM weather_history
        WHERE timestamp >= ?
        ORDER BY timestamp
    """, (cutoff,))
    rows = c.fetchall()
    conn.close()
    times, out_hum = [], []
    for t, out_h in rows:
        try:
            times.append(datetime.fromisoformat(t))
            out_hum.append(float(out_h) if out_h is not None else None)
        except Exception:
            continue
    return times, out_hum

def plot_humidity_graph(hours):
    times, out_hum = fetch_humidity_data(hours)
    if not times:
        print(f"No humidity data for last {hours} hours.")
        return
    plt.figure(figsize=(10,5), facecolor='#222831')
    ax = plt.gca()
    ax.set_facecolor('#222831')
    plt.plot(times, out_hum, label="Outdoor Humidity (%)", color="#00b4d8", linewidth=2)
    plt.title(f"Outdoor Humidity - Last {hours} Hour(s)", color='white', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Time", color='white', fontsize=13, fontweight='bold')
    plt.ylabel("Humidity (%)", color='white', fontsize=13, fontweight='bold')
    plt.legend(facecolor='#222831', frameon=False, fontsize=12, loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=2)
    plt.grid(True, linestyle='--', alpha=0.5, color='#393e46')
    if hours <= 24:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %I:%M %p'))
    plt.gcf().autofmt_xdate()
    ax.tick_params(colors='white', labelsize=11)
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.title.set_color('white')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color('white')
    plt.tight_layout(rect=[0,0.08,1,1])
    img_path = os.path.join(STATIC_DIR, f"humidity_line_{hours}h.png")
    plt.savefig(img_path, facecolor='#222831')
    plt.close()
    print(f"Saved {img_path}")

# --- Wind Spider Graphs ---
def fetch_wind_data(hours):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    c.execute(f"""
        SELECT timestamp, windSpeed_mph, windDir, windGust_mph, windGustDir FROM weather_history
        WHERE timestamp >= ?
        ORDER BY timestamp
    """, (cutoff,))
    rows = c.fetchall()
    conn.close()
    times, wind_speeds, wind_dirs, wind_gusts, wind_gust_dirs = [], [], [], [], []
    for t, ws, wd, wg, wgd in rows:
        try:
            times.append(datetime.fromisoformat(t))
            wind_speeds.append(float(ws) if ws is not None else 0)
            wind_dirs.append(float(wd) if wd is not None else 0)
            wind_gusts.append(float(wg) if wg is not None else 0)
            wind_gust_dirs.append(float(wgd) if wgd is not None else 0)
        except Exception:
            continue
    return times, wind_speeds, wind_dirs, wind_gusts, wind_gust_dirs

def plot_wind_spider_graph(hours):
    times, wind_speeds, wind_dirs, wind_gusts, wind_gust_dirs = fetch_wind_data(hours)
    if not times:
        print(f"No wind data for last {hours} hours.")
        return
    # Define compass bins (every 45°)
    compass_labels = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
    bin_edges = np.arange(-22.5, 361, 45)  # 8 bins, center at 0, 45, ...
    wind_bin_means = []
    gust_bin_means = []
    for i in range(len(compass_labels)):
        # Wind
        mask = [(d >= bin_edges[i]) and (d < bin_edges[i+1]) for d in wind_dirs]
        speeds = [s for s, m in zip(wind_speeds, mask) if m]
        wind_bin_means.append(np.mean(speeds) if speeds else 0)
        # Gust
        mask_g = [(d >= bin_edges[i]) and (d < bin_edges[i+1]) for d in wind_gust_dirs]
        gusts = [g for g, m in zip(wind_gusts, mask_g) if m]
        gust_bin_means.append(np.mean(gusts) if gusts else 0)
    # Close the polygon
    wind_bin_means += wind_bin_means[:1]
    gust_bin_means += gust_bin_means[:1]
    angles = np.deg2rad(np.arange(0, 361, 45))
    # Plot
    plt.figure(figsize=(7,7), facecolor='#444548')
    ax = plt.subplot(111, polar=True, facecolor='#444548')
    ax.plot(angles, wind_bin_means, '-', linewidth=3, color="#3887fa", label="Wind Speed")  # removed 'o-'
    ax.fill(angles, wind_bin_means, alpha=0.25, color="#3887fa")
    ax.plot(angles, gust_bin_means, '-', linewidth=3, color="#2ee59d", label="Gust Speed")  # removed 'o-'
    ax.fill(angles, gust_bin_means, alpha=0.18, color="#2ee59d")
    ax.set_theta_zero_location('N')
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.arange(0, 360, 45), compass_labels, color='white', fontsize=14, fontweight='bold')
    ax.set_title("Wind Vector", color='#7a8cff', fontsize=20, fontweight='bold', pad=25)
    # r-labels (speed)
    ax.set_rlabel_position(225)
    ax.yaxis.set_tick_params(color='white', labelcolor='white', labelsize=13)
    ax.grid(color='white', linestyle='-', linewidth=1.2, alpha=0.25)
    ax.spines['polar'].set_color('white')
    ax.spines['polar'].set_linewidth(2)
    # Legend
    legend = ax.legend(loc='lower left', bbox_to_anchor=(0.85, -0.05), frameon=False, fontsize=14)
    for text in legend.get_texts():
        text.set_color('white')
    plt.tight_layout(pad=3.0)
    img_path = os.path.join(STATIC_DIR, f"wind_vector_{hours}h.png")
    plt.savefig(img_path, facecolor='#444548')
    plt.close()
    print(f"Saved {img_path}")

# --- Solar Radiation Graphs ---
def fetch_solar_data(hours):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    c.execute(f"""
        SELECT timestamp, maxSolarRad_Wpm2 FROM weather_history
        WHERE timestamp >= ?
        ORDER BY timestamp
    """, (cutoff,))
    rows = c.fetchall()
    conn.close()
    times, solar = [], []
    for t, s in rows:
        try:
            times.append(datetime.fromisoformat(t))
            solar.append(float(s) if s is not None else None)
        except Exception:
            continue
    return times, solar

def plot_solar_graph(hours):
    times, solar = fetch_solar_data(hours)
    if not times:
        print(f"No solar data for last {hours} hours.")
        return
    plt.figure(figsize=(10,5), facecolor='#222831')
    ax = plt.gca()
    ax.set_facecolor('#222831')
    plt.plot(times, solar, label="Max Solar Radiation (W/m²)", color="#ffb703", linewidth=2)
    plt.title(f"Max Solar Radiation - Last {hours} Hour(s)", color='white', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Time", color='white', fontsize=13, fontweight='bold')
    plt.ylabel("Solar Radiation (W/m²)", color='white', fontsize=13, fontweight='bold')
    plt.legend(facecolor='#222831', frameon=False, fontsize=12, loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=2)
    plt.grid(True, linestyle='--', alpha=0.5, color='#393e46')
    if hours <= 24:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %I:%M %p'))
    plt.gcf().autofmt_xdate()
    ax.tick_params(colors='white', labelsize=11)
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.title.set_color('white')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color('white')
    plt.tight_layout(rect=[0,0.08,1,1])
    img_path = os.path.join(STATIC_DIR, f"solar_line_{hours}h.png")
    plt.savefig(img_path, facecolor='#222831')
    plt.close()
    print(f"Saved {img_path}")

# --- Rain Graphs ---
def fetch_rain_data(hours):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    c.execute(f"""
        SELECT timestamp, rain_total FROM weather_history
        WHERE timestamp >= ?
        ORDER BY timestamp
    """, (cutoff,))
    rows = c.fetchall()
    conn.close()
    times, rain_totals = [], []
    for t, r in rows:
        try:
            times.append(datetime.fromisoformat(t))
            rain_totals.append(float(r) if r is not None else None)
        except Exception:
            continue
    return times, rain_totals

def plot_rain_graph(hours):
    times, rain_totals = fetch_rain_data(hours)
    if not times or len(rain_totals) < 2:
        print(f"Not enough rain data for last {hours} hours.")
        return
    # Calculate rain per interval (difference between consecutive rain_total values)
    rain_per_interval = [max(r2 - r1, 0) if r1 is not None and r2 is not None else 0 for r1, r2 in zip(rain_totals[:-1], rain_totals[1:])]
    times_for_bars = times[1:]  # Each bar is for the interval ending at this time
    plt.figure(figsize=(10,5), facecolor='#222831')
    ax = plt.gca()
    ax.set_facecolor('#222831')
    ax.bar(times_for_bars, rain_per_interval, width=0.02*(hours), color="#3887fa", label="Rainfall (in)")
    plt.title(f"Rainfall - Last {hours} Hour(s)", color='white', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Time", color='white', fontsize=13, fontweight='bold')
    plt.ylabel("Rainfall (in)", color='white', fontsize=13, fontweight='bold')
    plt.legend(facecolor='#222831', frameon=False, fontsize=12, loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=2)
    plt.grid(True, linestyle='--', alpha=0.5, color='#393e46')
    if hours <= 24:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %I:%M %p'))
    plt.gcf().autofmt_xdate()
    ax.tick_params(colors='white', labelsize=11)
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.title.set_color('white')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color('white')
    plt.tight_layout(rect=[0,0.08,1,1])
    img_path = os.path.join(STATIC_DIR, f"rain_bar_{hours}h.png")
    plt.savefig(img_path, facecolor='#222831')
    plt.close()
    print(f"Saved {img_path}")

# --- Pressure Graphs ---
def fetch_pressure_data(hours):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    c.execute(f"""
        SELECT timestamp, pressure_inHg FROM weather_history
        WHERE timestamp >= ?
        ORDER BY timestamp
    """, (cutoff,))
    rows = c.fetchall()
    conn.close()
    times, pressures = [], []
    for t, p in rows:
        try:
            times.append(datetime.fromisoformat(t))
            pressures.append(float(p) if p is not None else None)
        except Exception:
            continue
    return times, pressures

def plot_pressure_graph(hours):
    times, pressures = fetch_pressure_data(hours)
    if not times:
        print(f"No pressure data for last {hours} hours.")
        return
    plt.figure(figsize=(10,5), facecolor='#222831')
    ax = plt.gca()
    ax.set_facecolor('#222831')
    plt.plot(times, pressures, label="Pressure (inHg)", color="#7a8cff", linewidth=2)
    plt.title(f"Pressure - Last {hours} Hour(s)", color='white', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Time", color='white', fontsize=13, fontweight='bold')
    plt.ylabel("Pressure (inHg)", color='white', fontsize=13, fontweight='bold')
    plt.legend(facecolor='#222831', frameon=False, fontsize=12, loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=2)
    plt.grid(True, linestyle='--', alpha=0.5, color='#393e46')
    if hours <= 24:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %I:%M %p'))
    plt.gcf().autofmt_xdate()
    ax.tick_params(colors='white', labelsize=11)
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.title.set_color('white')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color('white')
    plt.tight_layout(rect=[0,0.08,1,1])
    img_path = os.path.join(STATIC_DIR, f"pressure_line_{hours}h.png")
    plt.savefig(img_path, facecolor='#222831')
    plt.close()
    print(f"Saved {img_path}")

# --- Feels-Like Graphs ---
def fetch_feelslike_data(hours):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    cutoff = (datetime.now() - timedelta(hours=hours)).isoformat()
    c.execute(f"""
        SELECT timestamp, windchill_F, heatindex_F, appTemp_F FROM weather_history
        WHERE timestamp >= ?
        ORDER BY timestamp
    """, (cutoff,))
    rows = c.fetchall()
    conn.close()
    times, windchill, heatindex, appTemp = [], [], [], []
    for t, wc, hi, at in rows:
        try:
            times.append(datetime.fromisoformat(t))
            windchill.append(float(wc) if wc is not None else None)
            heatindex.append(float(hi) if hi is not None else None)
            appTemp.append(float(at) if at is not None else None)
        except Exception:
            continue
    return times, windchill, heatindex, appTemp

def plot_feelslike_graph(hours):
    times, windchill, heatindex, appTemp = fetch_feelslike_data(hours)
    if not times:
        print(f"No feels-like data for last {hours} hours.")
        return
    plt.figure(figsize=(10,5), facecolor='#222831')
    ax = plt.gca()
    ax.set_facecolor('#222831')
    plt.plot(times, windchill, label="Windchill (°F)", color="#3887fa", linewidth=2)
    plt.plot(times, heatindex, label="Heat Index (°F)", color="#ffb703", linewidth=2)
    plt.plot(times, appTemp, label="Apparent Temp (°F)", color="#2ee59d", linewidth=2)
    plt.title(f"Feels-Like Temperatures - Last {hours} Hour(s)", color='white', fontsize=16, fontweight='bold', pad=15)
    plt.xlabel("Time", color='white', fontsize=13, fontweight='bold')
    plt.ylabel("Temperature (°F)", color='white', fontsize=13, fontweight='bold')
    plt.legend(facecolor='#222831', frameon=False, fontsize=12, loc='lower center', bbox_to_anchor=(0.5, -0.25), ncol=3)
    plt.grid(True, linestyle='--', alpha=0.5, color='#393e46')
    if hours <= 24:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M %p'))
    else:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %I:%M %p'))
    plt.gcf().autofmt_xdate()
    ax.tick_params(colors='white', labelsize=11)
    ax.spines['top'].set_color('white')
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.spines['right'].set_color('white')
    ax.yaxis.label.set_color('white')
    ax.xaxis.label.set_color('white')
    ax.title.set_color('white')
    for label in ax.get_xticklabels() + ax.get_yticklabels():
        label.set_color('white')
    plt.tight_layout(rect=[0,0.08,1,1])
    img_path = os.path.join(STATIC_DIR, f"feelslike_line_{hours}h.png")
    plt.savefig(img_path, facecolor='#222831')
    plt.close()
    print(f"Saved {img_path}")

def main_loop():
    intervals = [1, 3, 6, 12]
    while True:
        for h in intervals:
            plot_temp_graph(h)
            plot_humidity_graph(h)
            plot_wind_spider_graph(h)
            plot_solar_graph(h)
            plot_rain_graph(h)
            plot_pressure_graph(h)
            plot_feelslike_graph(h)
        print("Sleeping 5 minutes...")
        time.sleep(300)

if __name__ == "__main__":
    main_loop()
