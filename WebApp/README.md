# Weather Data Visualization App

Веб-приложение для визуализации метеорологических данных. Загружает JSON файлы с метеоданными и отображает графики температуры, влажности, давления и скорости ветра.

## Установка и запуск

```bash
npm install
npm run dev
```

## Технологии
- React
- Zustand (стейт-менеджмент)
- Recharts (графики)
- Styled-components (стили)

## Формат JSON данных
```json
{
  "city": "String",
  "coordinates": {
    "lat": Number,
    "lon": Number
  },
  "daily_statistics": {
    "YYYY-MM-DD": {
      "temperature": {
        "min": Number,
        "max": Number,
        "avg": Number
      },
      "humidity": {
        "min": Number,
        "max": Number,
        "avg": Number
      },
      "pressure": {
        "min": Number,
        "max": Number,
        "avg": Number
      },
      "wind_speed": {
        "min": Number,
        "max": Number,
        "avg": Number
      }
    }
  }
}
```

## Структура проекта
```
src/
  ├── App.jsx
  ├── store.js
  └── components/
      ├── FileUpload.jsx
      └── WeatherCharts.jsx
```