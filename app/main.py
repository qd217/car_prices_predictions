import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from predict import processing
from schemas import CarInput

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/predict", response_class=HTMLResponse)
async def predict_view(
    request: Request,
    car_input: CarInput = Depends(CarInput.as_form),
):
    prediction = processing(**car_input.model_dump()) # {"Levy" : 123}

    '''prediction = processing(Levy, Manufacturer, Model, Prod_year, Category, Leather_interior,
                            Fuel_type, Engine_volume, Mileage, Cylinders, Gear_box_type,
                            Drive_wheels, Doors, Wheel, Color, Airbags)'''

    return templates.TemplateResponse("index.html", {
        "request": request,
        "prediction": round(prediction[0],0)
    })
