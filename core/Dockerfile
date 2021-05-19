FROM python:3.8.2

COPY ./core/requirements.txt .

RUN apt-get update \
    && apt-get install gcc g++ \
    && pip install --upgrade pip==20.0.2 \
    && pip install --upgrade setuptools==46.0.0 \
    && pip install -r requirements.txt

WORKDIR /usr/app

COPY ./core/ .
CMD ["python", "main.py"]
