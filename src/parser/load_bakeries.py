import json
import sqlite3

# --- Путь к JSON ---
json_file = "../jsons/bakeries.json"

# --- Подключение к SQLite ---
conn = sqlite3.connect("../geo_analysis.db")
cursor = conn.cursor()

# --- Создание таблиц ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS bakeries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    latitude REAL,
    longitude REAL
)
""")

# --- Загрузка JSON ---
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

unknowns_count = 0
for el in data.get("elements", []):
    tags = el.get("tags", {})
    name = tags.get("name", None)
    lat = el.get("lat")
    lon = el.get("lon")
    
    if name:
        cursor.execute(
            "INSERT INTO bakeries (name, latitude, longitude) VALUES (?, ?, ?)",
            (name, lat, lon)
        )
    else:
        unknowns_count += 1

conn.commit()
conn.close()

print("Данные успешно записаны в SQLite")
print("Количество Unknown пекарен: ", unknowns_count)