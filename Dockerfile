FROM python:3.8-alpine

WORKDIR /app

RUN apk add build-base postgresql-client postgresql-dev libffi-dev libressl-dev openssl-dev python-dev

COPY ./requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD gunicorn -w 4 -b :$PORT manage:app