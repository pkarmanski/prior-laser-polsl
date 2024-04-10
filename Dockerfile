FROM python:3.12.0
WORKDIR /app
COPY . /app
ENTRYPOINT ["python", "main.py"]
