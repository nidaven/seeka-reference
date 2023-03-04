FROM python:3.10.6-alpine3.16

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /src/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]


