import sqlite3
import csv
import os
<<<<<<< HEAD
import sys

def import_csv_to_db(csv_file_path, db_path):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()

    with open(csv_file_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            c.execute("""
                INSERT INTO weather_history (
                    DATE, HourlyAltimeterSetting, HourlyDewPointTemperature,
                    HourlyDryBulbTemperature, HourlyPrecipitation, HourlyRelativeHumidity,
                    HourlySeaLevelPressure, HourlyStationPressure, HourlyWetBulbTemperature,
                    HourlyWindDirection, HourlyWindGustSpeed, HourlyWindSpeed
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                row['DATE'], row['HourlyAltimeterSetting'], row['HourlyDewPointTemperature'],
                row['HourlyDryBulbTemperature'], row['HourlyPrecipitation'], row['HourlyRelativeHumidity'],
                row['HourlySeaLevelPressure'], row['HourlyStationPressure'], row['HourlyWetBulbTemperature'],
                row['HourlyWindDirection'], row['HourlyWindGustSpeed'], row['HourlyWindSpeed']
            ))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python import_csv.py <csv_file_path> <db_path>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    db_path = sys.argv[2]

    if not os.path.exists(csv_file_path):
        print(f"Error: CSV file '{csv_file_path}' does not exist.")
        sys.exit(1)

    if not os.path.exists(db_path):
        print(f"Error: Database file '{db_path}' does not exist.")
        sys.exit(1)

    try:
        import_csv_to_db(csv_file_path, db_path)
        print("CSV data imported successfully.")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
=======

# Path to the SQLite database
DB_PATH = os.getenv("SQLITE_PATH", "./data/weather.db")

# Path to the CSV file (update this to the actual file path)
CSV_FILE_PATH = "data/history.csv"

# Define a mapping from CSV columns to database columns
COLUMN_MAPPING = {
    "DATE": "timestamp",
    "HourlyAltimeterSetting": "altimeter_inHg",
    "HourlyDewPointTemperature": "dewpoint_F",
    "HourlyDryBulbTemperature": "outTemp_F",
    "HourlyPrecipitation": "rain_in",
    "HourlyRelativeHumidity": "outHumidity",
    "HourlySeaLevelPressure": "seaLevelPressure_inHg",
    "HourlyStationPressure": "stationPressure_inHg",
    "HourlyWetBulbTemperature": "wetBulbTemp_F",
    "HourlyWindDirection": "windDir",
    "HourlyWindGustSpeed": "windGust_mph",
    "HourlyWindSpeed": "windSpeed_mph"
}

def ensure_columns_exist(cursor, columns):
    """Ensure all columns in the CSV exist in the weather_history table."""
    for column in columns:
        try:
            cursor.execute(f"ALTER TABLE weather_history ADD COLUMN {column} REAL")
        except sqlite3.OperationalError:
            # Column already exists
            pass

def map_columns(row):
    """Map CSV columns to database columns using COLUMN_MAPPING."""
    mapped_row = {}
    for csv_col, db_col in COLUMN_MAPPING.items():
        if csv_col in row:
            mapped_row[db_col] = row[csv_col]
    return mapped_row

def import_csv_to_db():
    """Import data from a CSV file into the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Ensure the weather_history table exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_history (
            timestamp TEXT PRIMARY KEY
        )
    ''')

    with open(CSV_FILE_PATH, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        columns = reader.fieldnames

        # Ensure all columns exist in the table
        ensure_columns_exist(cursor, columns)

        for row in reader:
            # Map the columns using the mapping dictionary
            mapped_row = map_columns(row)

            # Prepare the data for insertion
            columns = list(mapped_row.keys())
            placeholders = ["?"] * len(columns)
            values = [mapped_row[col] for col in columns]

            # Insert the row into the table
            sql = f"INSERT OR REPLACE INTO weather_history ({', '.join(columns)}) VALUES ({', '.join(placeholders)})"
            cursor.execute(sql, values)

    conn.commit()
    conn.close()
    print(f"Data from {CSV_FILE_PATH} has been imported into the database.")

if __name__ == "__main__":
    import_csv_to_db()
>>>>>>> 911374b67fde846261b836efe2b30ad9ce388abf
