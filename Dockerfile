#FROM python:3.12
#WORKDIR /app
#COPY app .
#COPY requirements.txt .
#RUN pip install -r requirements.txt
#RUN python3 main.py

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY app/ .
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/app/app"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]