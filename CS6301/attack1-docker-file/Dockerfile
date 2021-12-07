# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /app

COPY attack1.py attack1.py

RUN pip install requests

CMD ["python3", "attack1.py"]
