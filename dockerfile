FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

COPY ./requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt
COPY ./app /app
