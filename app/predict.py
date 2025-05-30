import joblib
import pandas as pd

def processing(Levy, Manufacturer, Model, Prod_year, Category, Leather_interior, Fuel_type, Engine_volume, Mileage, Cylinders, Gear_box_type, Drive_wheels, Doors, Wheel, Color, Airbags):
  '''
  Логика модели
  '''
  # Формируем df по входным данным
  data = {
        'Levy': [Levy],
        'Manufacturer': [Manufacturer],
        'Model': [Model],
        'Prod. year': [Prod_year],
        'Category': [Category],
        'Leather interior': [Leather_interior],
        'Fuel type': [Fuel_type],
        'Engine volume': [Engine_volume],
        'Mileage': [Mileage],
        'Cylinders': [Cylinders],
        'Gear box type': [Gear_box_type],
        'Drive wheels': [Drive_wheels],
        'Doors': [Doors],
        'Wheel': [Wheel],
        'Color': [Color],
        'Airbags': [Airbags]
    }

  data = pd.DataFrame(data)

  # Загружаем энкодеры
  ordinal_encoder = joblib.load('for_model/ordinal_encoder.pkl')
  target_encoder = joblib.load('for_model/target_encoder.pkl')
  nominal_encoder = joblib.load('for_model/nominal_encoder.pkl')

  # Обрабатываем признаки
  ordinal_columns = ['Gear box type', 'Cylinders'] # Порядковые значения
  high_cardinality_columns = ['Model', 'Manufacturer', 'Engine volume'] # Признаки с высокой кардинальностью
  low_cardinality_columns = ['Fuel type', 'Color', 'Drive wheels', 'Category', 'Leather interior', 'Doors', 'Wheel'] # Признаки с малой кардинальностью

  # Явно задаём типы данных
  data['Levy'] = data['Levy'].astype('int64')
  data['Manufacturer'] = data['Manufacturer'].astype('object') 
  data['Model'] = data['Model'].astype('object')  
  data['Prod. year'] = data['Prod. year'].astype('int64')
  data['Category'] = data['Category'].astype('object')  
  data['Leather interior'] = data['Leather interior'].astype('object')  
  data['Fuel type'] = data['Fuel type'].astype('object')  
  data['Engine volume'] = data['Engine volume'].astype('object')  
  data['Mileage'] = data['Mileage'].astype('int64')
  data['Cylinders'] = data['Cylinders'].astype('float64')
  data['Gear box type'] = data['Gear box type'].astype('object')
  data['Drive wheels'] = data['Drive wheels'].astype('object')
  data['Doors'] = data['Doors'].astype('object')
  data['Wheel'] = data['Wheel'].astype('object')
  data['Color'] = data['Color'].astype('object')
  data['Airbags'] = data['Airbags'].astype('int64')

  data[ordinal_columns] = ordinal_encoder.transform(data[ordinal_columns])
  data[high_cardinality_columns] = target_encoder.transform(data[high_cardinality_columns])
  data[low_cardinality_columns] = nominal_encoder.transform(data[low_cardinality_columns])

  # Явно задаём типы данных
  data['Levy'] = data['Levy'].astype('int64')
  data['Manufacturer'] = data['Manufacturer'].astype('float64') 
  data['Model'] = data['Model'].astype('float64')  
  data['Prod. year'] = data['Prod. year'].astype('int64')
  data['Category'] = data['Category'].astype('float64')  
  data['Leather interior'] = data['Leather interior'].astype('float64')  
  data['Fuel type'] = data['Fuel type'].astype('float64')  
  data['Engine volume'] = data['Engine volume'].astype('float64')  
  data['Mileage'] = data['Mileage'].astype('int64')
  data['Cylinders'] = data['Cylinders'].astype('float64')
  data['Gear box type'] = data['Gear box type'].astype('float64')
  data['Drive wheels'] = data['Drive wheels'].astype('float64')
  data['Doors'] = data['Doors'].astype('float64')
  data['Wheel'] = data['Wheel'].astype('float64')
  data['Color'] = data['Color'].astype('float64')
  data['Airbags'] = data['Airbags'].astype('int64')

  # Загружаем модель и получаем предсказание
  model = joblib.load('for_model/xgb_model.pkl')
  prediction = model.predict(data)

  return prediction
