import requests
import sqlite3
import time

# --- Overpass API ---
OVERPASS_URL = "https://overpass-api.de/api/interpreter"

def safe_request(query, timeout=60, retries=3):
    """Делает запрос к Overpass API с retry логикой"""
    for attempt in range(retries):
        try:
            response = requests.post(OVERPASS_URL, data=query, timeout=timeout)
            print(f"Response status: {response.status_code}")
            if response.status_code == 200:
                return response.json()
            else:
                print(f"  Server error {response.status_code}, retrying... ({attempt+1}/{retries})")
                time.sleep(5)
        except Exception as e:
            print(f"  Error: {e}, retrying... ({attempt+1}/{retries})")
            time.sleep(5)
    return {"elements": []}


# Екатеринбург (примерный bounding box) - расширенная площадь
CITY_BBOX = "56.75,60.35,56.95,60.75"

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

metro_response = safe_request(metro_query)

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

# --- Запрос пекарен (все) ---
bakery_query = f"""
[out:json];
(
  node["shop"="bakery"]({CITY_BBOX});
  way["shop"="bakery"]({CITY_BBOX});
);
out body;
"""

bakery_response = safe_request(bakery_query)

for el in bakery_response["elements"]:
    if el["type"] == "node":
        cursor.execute(
            "INSERT INTO bakeries (name, latitude, longitude) VALUES (?, ?, ?)",
            (
                el.get("tags", {}).get("name"),
                el["lat"],
                el["lon"]
            )
        )
    elif el["type"] == "way":
        # Для ways берём центроид (среднее координат всех узлов)
        lat_avg = sum(node.get("lat", 0) for node in el.get("geometry", [])) / max(len(el.get("geometry", [])), 1)
        lon_avg = sum(node.get("lon", 0) for node in el.get("geometry", [])) / max(len(el.get("geometry", [])), 1)
        cursor.execute(
            "INSERT INTO bakeries (name, latitude, longitude) VALUES (?, ?, ?)",
            (
                el.get("tags", {}).get("name"),
                lat_avg,
                lon_avg
            )
        )

# --- Запрос остановок транспорта ---
stops_query = f"""
[out:json];
(
  node["public_transport"="stop_position"]({CITY_BBOX});
  node["highway"="bus_stop"]({CITY_BBOX});
  node["railway"="tram_stop"]({CITY_BBOX});
  node["railway"="halt"]({CITY_BBOX});
);
out body;
"""

stops_response = safe_request(stops_query)

for el in stops_response["elements"]:
    cursor.execute(
        "INSERT INTO infrastructure (type, name, latitude, longitude) VALUES (?, ?, ?, ?)",
        (
            "stop",
            el.get("tags", {}).get("name", "Unknown Stop"),
            el["lat"],
            el["lon"]
        )
    )

conn.commit()

# --- Проверка данных ---
print("\n=== Проверка загруженных данных ===")

metro_count = cursor.execute("SELECT COUNT(*) FROM infrastructure WHERE type='metro'").fetchone()[0]
print(f"Метро: {metro_count} станций")

stop_count = cursor.execute("SELECT COUNT(*) FROM infrastructure WHERE type='stop'").fetchone()[0]
print(f"Остановки: {stop_count} остановок")

bakery_count = cursor.execute("SELECT COUNT(*) FROM bakeries").fetchone()[0]
print(f"Пекарни: {bakery_count} пекарен")

# Примеры данных
print("\n--- Примеры метро ---")
metro_samples = cursor.execute("SELECT name, latitude, longitude FROM infrastructure WHERE type='metro' LIMIT 3").fetchall()
for row in metro_samples:
    print(f"  {row[0]} ({row[1]}, {row[2]})")

print("\n--- Примеры остановок ---")
stop_samples = cursor.execute("SELECT name, latitude, longitude FROM infrastructure WHERE type='stop' LIMIT 3").fetchall()
for row in stop_samples:
    print(f"  {row[0]} ({row[1]}, {row[2]})")

print("\n--- Примеры пекарен ---")
bakery_samples = cursor.execute("SELECT name, latitude, longitude FROM bakeries LIMIT 3").fetchall()
for row in bakery_samples:
    print(f"  {row[0]} ({row[1]}, {row[2]})")

conn.close()

print("\n✓ Данные успешно загружены в базу данных!")
