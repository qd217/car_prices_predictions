import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from predict import processing
from schemas import CarInput
from fastapi.staticfiles import StaticFiles
from sqlalchemy import insert, select
from models import UserCarInput, session
from sqlalchemy.orm import Session
import redis.asyncio as redis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

app = FastAPI()

templates = Jinja2Templates(directory="templates") # Для рендеринга HTML
app.mount("/static", StaticFiles(directory="static"), name="static") # Настройка сервера так, чтобы он обслуживал статические файлы из папки "static"

@app.get("/", response_class=HTMLResponse) # Обозначаем путь для начальной страницы и тип запроса (get)
#@cache(expire=60) # Кешируем ответ на 60 сек.
async def home(request: Request):
    '''
    Открывает начальную страницу index.html
    :param request: входящий запрос; объект, в котором содержаться данные из браузера,
    необходимые для взаисодействия браузера-пользователя
    :return: "отрендеренная html страница", т.е. данные о взаимодействии от пользователя в html документе
    '''
    content = templates.get_template('index.html').render({"request": request}) # Готовый HTML-код страницы index.html с учётом переданных данных (request).
    # Передача в шаблон request — стандартная практика для корректной работы и удобства шаблонов.
    return HTMLResponse(content)

@app.get("/history", response_class=HTMLResponse) # Путь к странице с историей
#@cache(expire=60) # Кешируем ответ на 60 сек.
async def hist(request: Request):
    '''
    Открывает страницу с историей table.html
    :param request: входящий запрос; объект, в котором содержаться данные из браузера,
    необходимые для взаисодействия браузера-пользователя
    :return: "отрендеренная html страница", т.е. данные о взаимодействии от пользователя в html документе
    '''
    select_from_table = [el.__dict__ for el in select_user_data(session)]
    content = templates.get_template('table.html').render({"request": request, "data": select_from_table})
    return HTMLResponse(content)

@cache(expire=60)
async def get_cached_history():
    '''
    Получает и кеширует данные истории
    :return: список записей истории
    '''
    records = select_user_data(session)
    return [{
        "id": record.id,
        "levy": record.levy,
        "manufacturer": record.manufacturer,
        "model": record.model,
        "prod_year": record.prod_year,
        "category": record.category,
        "leather_interior": record.leather_interior,
        "fuel_type": record.fuel_type,
        "engine_volume": record.engine_volume,
        "mileage": record.mileage,
        "cylinders": record.cylinders,
        "gear_box_type": record.gear_box_type,
        "drive_wheels": record.drive_wheels,
        "doors": record.doors,
        "wheel": record.wheel,
        "color": record.color,
        "airbags": record.airbags,
        "result": record.result
    } for record in records]

@app.post("/predict", response_class=HTMLResponse)
async def predict_view(
    request: Request,
    car_input: CarInput = Depends(CarInput.as_form), # Depends связывает данные из формы с моделью CarInpu
):
    '''
    Обрабатывает POST-запрос с данными формы. На основе входных данных (характеристики автомобиля) возвращает
    предсказанную цену и отображает её на странице. Одновременно сохраняет данные в базу.
    :param request: входящий запрос; объект, в котором содержаться данные из браузера,
    необходимые для взаисодействия браузера-пользователя
    :param car_input: модель формы с параметрами авто, полученными от пользователя
    :return: index.html с полем "prediction" — результатом работы ML-модели.
    '''
    # Преобразуем pydantic модель в словарь с правильными именами параметров
    input_dict = {
        'Levy': car_input.Levy,
        'Manufacturer': car_input.Manufacturer,
        'Model': car_input.Model,
        'Prod. year': car_input.Prod_year,
        'Category': car_input.Category,
        'Leather interior': car_input.Leather_interior,
        'Fuel type': car_input.Fuel_type,
        'Engine volume': car_input.Engine_volume,
        'Mileage': car_input.Mileage,
        'Cylinders': car_input.Cylinders,
        'Gear box type': car_input.Gear_box_type,
        'Drive wheels': car_input.Drive_wheels,
        'Doors': car_input.Doors,
        'Wheel': car_input.Wheel,
        'Color': car_input.Color,
        'Airbags': car_input.Airbags
    }

    prediction = await get_cached_prediction(**input_dict)
#    prediction = processing(**car_input.model_dump()) # {"Levy" : 123}

    '''prediction = processing(Levy, Manufacturer, Model, Prod_year, Category, Leather_interior,
                            Fuel_type, Engine_volume, Mileage, Cylinders, Gear_box_type,
                            Drive_wheels, Doors, Wheel, Color, Airbags)'''
    # Заносим запрос в базу
    user_dict = {
        "levy": car_input.Levy,
        "manufacturer": car_input.Manufacturer,
        "model": car_input.Model,
        "prod_year": car_input.Prod_year,
        "category": car_input.Category,
        "leather_interior": car_input.Leather_interior,
        "fuel_type": car_input.Fuel_type,
        "engine_volume": car_input.Engine_volume,
        "mileage": car_input.Mileage,
        "cylinders": car_input.Cylinders,
        "gear_box_type": car_input.Gear_box_type,
        "drive_wheels": car_input.Drive_wheels,
        "doors": car_input.Doors,
        "wheel": car_input.Wheel,
        "color": car_input.Color,
        "airbags": car_input.Airbags,
        "result":float(round(prediction[0],0))
    }
    insert_user_data(session, user_dict)

    # Выводим на странице ответ
    return templates.TemplateResponse("index.html", {
        "request": request,
        "prediction": round(prediction[0],0)
    })

@cache(expire=60)
async def get_cached_prediction(**kwargs):
    '''
    Получает и кеширует результат предсказания
    :param kwargs: параметры для предсказания
    :return: результат предсказания
    '''
    result = processing(
        Levy=kwargs['Levy'],
        Manufacturer=kwargs['Manufacturer'],
        Model=kwargs['Model'],
        Prod_year=kwargs['Prod. year'],
        Category=kwargs['Category'],
        Leather_interior=kwargs['Leather interior'],
        Fuel_type=kwargs['Fuel type'],
        Engine_volume=kwargs['Engine volume'],
        Mileage=kwargs['Mileage'],
        Cylinders=kwargs['Cylinders'],
        Gear_box_type=kwargs['Gear box type'],
        Drive_wheels=kwargs['Drive wheels'],
        Doors=kwargs['Doors'],
        Wheel=kwargs['Wheel'],
        Color=kwargs['Color'],
        Airbags=kwargs['Airbags']
    )
    return result.tolist()  # Конвертируем numpy array в список для JSON сериализации

def insert_user_data(session: Session, user_dict: dict):
    '''
    Вставляет данные об автомобиле, введённые пользователем, в таблицу UserCarInput в базе данных.
    :param session: Сессия
    :param user_dict: Данные по авто
    :return:
    '''
    stmt = insert(UserCarInput).values(**user_dict) # Создание SQL-запроса INSERT
    session.execute(stmt) # Выполнение запроса
    session.commit() # Подтверждение изменений

def select_user_data(session: Session):
    '''
    Извлекает все строки из таблицы UserCarInput и возвращает их в виде списка объектов ORM-модели.
    :param session: Сессия
    :return: Данные по авто
    '''
    stmt = select(UserCarInput)
    return session.scalars(stmt).all() # [row[0] for row in session.execute(stmt).fetchall())
# [(user_input, ), (), ()]

@app.on_event("startup")
async def startup_event():
    '''
    Автоматически вызывается при старте FastAPI-приложения. Она настраивает Redis-клиент и
    инициализирует систему кеширования FastAPI через FastAPICache
    '''
    redis_client = redis.Redis(
        host="redis",  # Имя сервиса из docker-compose
        port=6379, # Стандартный порт redis
        decode_responses=False # Данные в байтах, без автоматического декодирования.
        )
    await redis_client.ping() # Проверка связи с redis
    FastAPICache.init(RedisBackend(redis_client), prefix="fastapi-cache") # Инициализация кэша

