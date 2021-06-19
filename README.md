![Build Status](https://github.com/unexpectedjourney/numerai-experiments-wrapper/actions/workflows/tests.yml/badge.svg?branch=main)

# numeria-experiments-wrapper

This project contains the implementation of numeria experiments web-wrapper, which is a final project for UCU Software Architecture for Data Science in Python.

## Authors
- Anton Babenko
- Volodymyr Prypeshniuk

## Project summary
This project contains several important parts:
- api - API service to get users requests;
- core - workers, which executes users requests according to numerai competition;
- web - web interface, which is the SPA page.
- mongodb - storage;
- rabbitmq - queue which delivers tasks to workers.

The architecture is a microservice one.

## Build
This project is working with Docker, so for good work, you should have such applications as:
1. docker
2. docker-compose

### To build this project, please use:
```
docker-compose build
```

### To up such project use:
```
docker-compose up
```

### Environment file
To work with the project, you should create `.env` file based on `.env.example`

### Data fiels
Please dowload data from the numerai competition and place them as __train.csv__ and __test.csv__ files in the data folder.
