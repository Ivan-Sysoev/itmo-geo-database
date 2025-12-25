import sqlite3
import csv

# Подключение к базе
conn = sqlite3.connect("../geo_analysis.db")
cursor = conn.cursor()

# --- Экспорт таблицы bakeries ---
cursor.execute("SELECT * FROM bakeries")
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]

with open("../../csv/bakeries.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(columns)  # заголовки
    writer.writerows(rows)

print("Таблица bakeries экспортирована в bakeries.csv")

# --- Экспорт таблицы infrastructure ---
cursor.execute("SELECT * FROM infrastructure")
rows = cursor.fetchall()
columns = [description[0] for description in cursor.description]

with open("../../csv/infrastructure.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(columns)  # заголовки
    writer.writerows(rows)

print("Таблица infrastructure экспортирована в infrastructure.csv")

conn.close()
