FROM python:3.9

COPY requirements.txt /

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 5000

WORKDIR /app

CMD exec gunicorn -b 0.0.0.0:5000 --timeout=9000 'wsgi:create_app()'