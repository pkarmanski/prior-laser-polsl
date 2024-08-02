FROM python:3.9
ENV PYTHONUNBUFFERED=1

RUN apt-get update && \
    apt-get install -y libgl1-mesa-glx libxkbcommon-x11-0 libxcb1 libx11-6 libxext6 libxrender1 libxcb-xinerama0 \
                       libqt5gui5 libqt5core5a libqt5widgets5 libglib2.0-0 libsm6 libice6 libxau6 libxdmcp6 \
                       libxcomposite1 libxcursor1 libxdamage1 libxi6 libxtst6 libnss3 libxss1 libatk1.0-0 \
                       libpango1.0-0 libatk-bridge2.0-0 libgdk-pixbuf2.0-0 libxcb-xinerama0-dev && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY installation/freeze.cfg /app/
RUN pip install --no-cache-dir -r freeze.cfg

COPY . /app
CMD ["python", "main.py"]
