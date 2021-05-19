FROM python:3.8.2-alpine3.11

COPY ./api/requirements.txt .

RUN apk update \
    && apk add gcc g++ libffi-dev openssl-dev jpeg-dev zlib-dev build-base linux-headers \
    && pip install --upgrade pip==20.0.2 \
    && pip install --upgrade setuptools==46.0.0 \
    && pip install -r requirements.txt

WORKDIR /usr/app

COPY ./api/ .
CMD ["python", "main.py"]
