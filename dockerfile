FROM python:3.9

WORKDIR /code
COPY ./app/requirements.txt /code/requirements.txt
RUN pip3 install --no-cache-dir --upgrade -r /code/app/requirements.txt
COPY ./app /code/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8088"]