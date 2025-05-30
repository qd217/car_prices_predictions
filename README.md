# Machine Learning Web App
## Описание
Это веб-приложение для предсказания цены автомобиля на основе обученной модели XGBoost. Приложение использует FastAPI для бэкенда, HTML/CSS/JS для фронтенда, и Docker для контейнеризации.

## Технологии
- FastAPI - современный веб-фреймворк для создания API
- SQLAlchemy - ORM для работы с базой данных
- PostgreSQL - база данных для хранения истории предсказаний
- Redis - кэширование результатов предсказаний
- Docker & Docker Compose - контейнеризация приложения
- XGBoost - модель машинного обучения для предсказания цен

## Обучение модели

Обучение модели XGBoost проводилось в Jupyter Notebook. Вы можете ознакомиться с полным процессом подготовки данных, энкодинга и обучения по следующей ссылке:
https://colab.research.google.com/drive/1abHlelC_c5Bm8Vza9EVkdjpF4dLGNKfB#scrollTo=9M0A6iyRXq7j
После обучения модель и энкодеры были сериализованы и сохранены в папку `app/for_model/`.

## Структура проекта

```plaintext
app/
├── for_model/
│   ├── nominal_encoder.pkl
│   ├── ordinal_encoder.pkl
│   ├── target_encoder.pkl
│   └── xgb_model.pkl
│
├── static/
│   ├── script.js
│   └── styles.css
│
├── templates/
│   ├── index.html
│   └── table.html
│
├── __init__.py
├── main.py
├── models.py
├── predict.py
├── schemas.py
│
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Запуск проекта
### Клонирование репозиторий

```bash
git clone https://github.com/qd217/car_prices_predictions
cd car_prices_predictions
```

### Создание файла .env
Переменные файла .env:
```plantext
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_database_name
```

### Сборка и запуск docker-контейнера
```bash
docker compose up --build
```

## API
```plantext
### GET "/"
- Описание: Открывает главную страницу с формой для ввода параметров автомобиля
- Ответ: HTML страница

### GET "/history"
- Описание: Открывает страницу с историей предсказаний
- Ответ: HTML страница с таблицей предыдущих предсказаний

### POST "/predict"
- Описание: Принимает параметры автомобиля и возвращает предсказанную цену
- Тело запроса: Form данные с параметрами автомобиля
- Ответ: HTML страница с результатом предсказания
```

