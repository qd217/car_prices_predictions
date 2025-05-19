from typing import Type

from fastapi import Form
from pydantic import BaseModel

def as_form(cls: Type[BaseModel]):
    new_params = {
        field.name: (Form(field.default) if field.default is not None else Form(...))
        for field in cls.__fields__.values()
    }
    return type(cls.__name__, (cls,), {"__annotations__": cls.__annotations__, **new_params})


#@as_form
class CarInput(BaseModel):
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
    Doors: str
    Wheel: str
    Color: str
    Airbags: int

