FROM python:3.8

WORKDIR /usr/home/flask
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8000
COPY . .
CMD ["gunicorn","--config", "gunicorn_config.py", "main:app"]