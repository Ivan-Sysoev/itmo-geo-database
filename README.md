# 5) Гео-анализ "близости к инфраструктуре"
### Близость пекарен к станциям метро в городе Екатеринбург

---

## Используемые API:
* `OpenStreetMap (Overpass API)`

---

## Структура базы данных

1. Пекарни

```sql
bakeries (
    id SERIAL PRIMARY KEY,
    name TEXT,
    chain TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
)
```

2. Инфраструктура

```sql
infrastructure (
    id SERIAL PRIMARY KEY,
    type TEXT,
    name TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
)
```

3. Результаты геоанализа

```sql
bakery_proximity (
    bakery_id INT REFERENCES bakeries(id),
    infrastructure_id INT REFERENCES infrastructure(id),
    distance_meters DOUBLE PRECISION,
    PRIMARY KEY (bakery_id, infrastructure_id)
)
```

## Parsing

Получение данных и запись в базу данных будет происходить с помощью:
* Языка программирования `Python` и библиотеки `requests`

## Анализ и визуализация данных 

Анализ данных будет проводиться при помощи:
* `языка SQL`

Визуализация данных при помощи:
* `Yandex DataLens`
