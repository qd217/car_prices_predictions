from pydantic import BaseModel
from fastapi import Form

class CarInput(BaseModel):
    '''
    Создаётся Pydantic-модель для корректного заполнения данных
    '''
    Levy: int
    Manufacturer: str
    Model: str
    Prod_year: int
    Category: str
    Leather_interior: str
    Fuel_type: str
    Engine_volume: str
    Mileage: int
    Cylinders: float
    Gear_box_type: str
    Drive_wheels: str
    Doors: int
    Wheel: str
    Color: str
    Airbags: int

    @classmethod
    def as_form(
        cls,
        Levy: int             = Form(...),
        Manufacturer: str     = Form(...),
        Model: str            = Form(...),
        Prod_year: int        = Form(...),
        Category: str         = Form(...),
        Leather_interior: str = Form(...),
        Fuel_type: str        = Form(...),
        Engine_volume: str    = Form(...),
        Mileage: int          = Form(...),
        Cylinders: float      = Form(...),
        Gear_box_type: str    = Form(...),
        Drive_wheels: str     = Form(...),
        Doors: int            = Form(...),
        Wheel: str            = Form(...),
        Color: str            = Form(...),
        Airbags: int          = Form(...),
    ) -> "CarInput":
        '''
        Для приема данных из HTML-формы, т.к. FastAPI по умолчанию принимает JSON в теле POST-запросов.
        '''
        return cls(
            Levy=Levy,
            Manufacturer=Manufacturer,
            Model=Model,
            Prod_year=Prod_year,
            Category=Category,
            Leather_interior=Leather_interior,
            Fuel_type=Fuel_type,
            Engine_volume=Engine_volume,
            Mileage=Mileage,
            Cylinders=Cylinders,
            Gear_box_type=Gear_box_type,
            Drive_wheels=Drive_wheels,
            Doors=Doors,
            Wheel=Wheel,
            Color=Color,
            Airbags=Airbags,
        )