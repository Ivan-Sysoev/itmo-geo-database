import requests
import sqlite3

# --- Overpass API ---
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

# Екатеринбург (примерный bounding box)
CITY_BBOX = "56.80,60.45,56.90,60.65"

# --- SQL ---
conn = sqlite3.connect("../geo_analysis.db")
cursor = conn.cursor()

# Таблицы
cursor.execute("""
CREATE TABLE IF NOT EXISTS bakeries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    latitude REAL,
    longitude REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS infrastructure (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    type TEXT,
    name TEXT,
    latitude REAL,
    longitude REAL
)
""")

# --- Запрос метро ---
metro_query = f"""
[out:json];
node["railway"="station"]["station"="subway"]({CITY_BBOX});
out body;
"""

metro_response = requests.post(OVERPASS_URL, data=metro_query).json()

for el in metro_response["elements"]:
    cursor.execute(
        "INSERT INTO infrastructure (type, name, latitude, longitude) VALUES (?, ?, ?, ?)",
        (
            "metro",
            el.get("tags", {}).get("name"),
            el["lat"],
            el["lon"]
        )
    )

# --- Запрос пекарен (берём первые 5) ---
bakery_query = f"""
[out:json];
node["shop"="bakery"]({CITY_BBOX});
out body 5;
"""

bakery_response = requests.post(OVERPASS_URL, data=bakery_query).json()

for el in bakery_response["elements"]:
    cursor.execute(
        "INSERT INTO bakeries (name, latitude, longitude) VALUES (?, ?, ?)",
        (
            el.get("tags", {}).get("name"),
            el["lat"],
            el["lon"]
        )
    )

conn.commit()
conn.close()

print("Данные успешно загружены в базу данных!")
