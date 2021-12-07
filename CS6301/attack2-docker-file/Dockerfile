# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY attack2.py attack2.py

RUN pip install requests

CMD ["python3", "attack2.py"]
