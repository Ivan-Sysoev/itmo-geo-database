import sqlite3
import math

RADIUS = 400

# --- Функция Haversine ---
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000  # радиус Земли в метрах
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    c = 2*math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# --- Подключение к SQLite ---
conn = sqlite3.connect("../geo_analysis.db")
cursor = conn.cursor()

# --- Создаём таблицу bakery_proximity ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS bakery_proximity (
    bakery_id INTEGER,
    infrastructure_id INTEGER,
    distance_meters REAL
)
""")

# --- Получаем все пекарни и инфраструктуру ---
cursor.execute("SELECT id, latitude, longitude FROM bakeries")
bakeries = cursor.fetchall()

cursor.execute("SELECT id, latitude, longitude FROM infrastructure")
infra = cursor.fetchall()


# --- Вычисляем расстояния и фильтруем по радиусу ---
for b_id, b_lat, b_lon in bakeries:
    for i_id, i_lat, i_lon in infra:
        d = haversine(b_lat, b_lon, i_lat, i_lon)
        if d <= RADIUS:
            cursor.execute(
                "INSERT INTO bakery_proximity (bakery_id, infrastructure_id, distance_meters) VALUES (?, ?, ?)",
                (b_id, i_id, d)
            )

conn.commit()
conn.close()

print(f"Таблица bakery_proximity заполнена: только объекты в радиусе {RADIUS} м")
