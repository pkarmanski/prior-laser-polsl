FROM python:3.12.0
WORKDIR /app
COPY . /app
RUN pip install -r installation/freeze.cfg
ENTRYPOINT ["python", "main.py"]
