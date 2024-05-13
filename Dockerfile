FROM python:3.12.0
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libglib2.0-0
RUN pip install -r installation/freeze.cfg
ENTRYPOINT ["python", "main.py"]
