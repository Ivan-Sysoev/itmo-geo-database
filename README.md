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
    type TEXT,           -- metro / bus_stop / tram_stop
    name TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION
)
```

3. Результаты геоанализа

```sql
bakery_proximity (
    bakery_id INTEGER REFERENCES bakeries(id),
    infrastructure_id INTEGER REFERENCES infrastructure(id),
    distance_meters DOUBLE PRECISION
)
```

## Parsing

Получение данных и запись в базу данных будет происходить с помощью:
* Языка программирования `Python` и библиотеки `requests`
* [`GUI Overpass Turbo`](https://overpass-turbo.eu/)

## Анализ и визуализация данных 

Анализ данных будет проводиться при помощи:
* `Языка SQL`
* `Субд SQLite`

Визуализация данных при помощи:
* `Yandex DataLens`

## Overpass API queries

1. Пекарни:

```js
[out:json][timeout:50];
area["name"="Екатеринбург"]->.city;
(
  node["shop"="bakery"](area.city);
  node["shop"="coffee"](area.city);
  node["shop"="confectionery"](area.city);
  node["amenity"="cafe"](area.city);
);
out body;
```

2. Станции метро и Остановки общественного транспорта

```js
[out:json][timeout:50];
area["name"="Екатеринбург"]->.city;
(
  node["railway"="station"]["station"="subway"];
  node["public_transport"="stop_position"];
);
out body;
```