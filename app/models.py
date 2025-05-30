from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base, Mapped, mapped_column
from dotenv import dotenv_values

config = dotenv_values(".env") # Чтение файла .env

db_url = f"postgresql://{config['POSTGRES_USER']}:{config['POSTGRES_PASSWORD']}@postgresql:5432/{config['POSTGRES_DB']}" # Параметры подключения к PostgreSQL

engine = create_engine(db_url) # Создание движка

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) # Сессия для запросов (класс)

session = SessionLocal() # Создание сессии подключения к базе данных

Base = declarative_base() # Конструкция SQLAlchemy ORM для работы с базами данных через Python-классы

class UserCarInput(Base):
    '''
    Модель/таблица для хранения введенных данных
    '''
    __tablename__ = "user_car_inputs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    levy: Mapped[int] = mapped_column(nullable=True)
    manufacturer: Mapped[str] = mapped_column(nullable=True)
    model: Mapped[str] = mapped_column(nullable=True)
    prod_year: Mapped[int] = mapped_column(nullable=True)
    category: Mapped[str] = mapped_column(nullable=True)
    leather_interior: Mapped[str] = mapped_column(nullable=True)
    fuel_type: Mapped[str] = mapped_column(nullable=True)
    engine_volume: Mapped[str] = mapped_column(nullable=True)
    mileage: Mapped[int] = mapped_column(nullable=True)
    cylinders: Mapped[float] = mapped_column(nullable=True)
    gear_box_type: Mapped[str] = mapped_column(nullable=True)
    drive_wheels: Mapped[str] = mapped_column(nullable=True)
    doors: Mapped[str] = mapped_column(nullable=True)
    wheel: Mapped[str] = mapped_column(nullable=True)
    color: Mapped[str] = mapped_column(nullable=True)
    airbags: Mapped[int] = mapped_column(nullable=True)
    result: Mapped[int] = mapped_column(nullable=True)

Base.metadata.create_all(engine) # Создение таблицы
