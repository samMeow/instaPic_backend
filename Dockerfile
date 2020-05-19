FROM python:3.8-alpine

WORKDIR /app

RUN apk add build-base postgresql-client postgresql-dev libffi-dev libressl-dev openssl-dev python-dev

COPY . /app

RUN pip install -r requirements.txt

CMD ["python", "manage.py", "run"]