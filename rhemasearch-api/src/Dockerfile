FROM python:3.10.6-alpine3.16

# Add environment variables
ENV PYTHONUNBUFFERED=1

ARG api_key
ENV OPENAI_API_KEY=$api_key

ARG db_fqdn_url
ENV DB_FQDN=$db_fqdn_url

WORKDIR /src

COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /src/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]


