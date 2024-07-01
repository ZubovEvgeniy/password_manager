FROM python:3.9-slim

RUN mkdir /app

COPY requirements.txt /app

RUN pip3 install -r /app/requirements.txt --no-cache-dir

COPY password_manager/ /app

WORKDIR /app

CMD ["gunicorn", "password_manager.wsgi:application", "--bind", "0:8000" ]