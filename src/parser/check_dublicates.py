import sqlite3

# Подключаемся к базе
conn = sqlite3.connect("../geo_analysis.db")
cursor = conn.cursor()

# --- Проверка дубликатов в bakeries ---
cursor.execute("""
SELECT COUNT(*) - COUNT(DISTINCT latitude || '-' || longitude) AS duplicate_count
FROM bakeries
""")
bakeries_duplicates = cursor.fetchone()[0]
print(f"Количество дубликатов в bakeries: {bakeries_duplicates}")

# --- Проверка дубликатов в infrastructure ---
cursor.execute("""
SELECT COUNT(*) - COUNT(DISTINCT latitude || '-' || longitude) AS duplicate_count
FROM infrastructure
""")
infra_duplicates = cursor.fetchone()[0]
print(f"Количество дубликатов в infrastructure: {infra_duplicates}")

conn.close()
