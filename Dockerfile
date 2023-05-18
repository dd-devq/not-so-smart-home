FROM python:3.10-alpine

RUN mkdir /app
WORKDIR /app

EXPOSE 5000

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "app.py"]