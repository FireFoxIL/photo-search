FROM python:3.7

EXPOSE 80

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install uwsgi
COPY ./requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir
COPY . .

CMD ./wait-for-it.sh ${DB_HOST}:${DB_PORT} -t 10 && \
    python manage.py migrate && \
    uwsgi --ini uwsgi.ini
