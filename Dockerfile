FROM python:3.10
ENV LANG=C.UTF-8

WORKDIR /app

COPY . /app

RUN : \
    && apt-get update \
    && apt-get install -y wget unzip \
    && pip install --no-cache-dir -r requirements.txt \
    # Not sure this is needed anymore with Selenium Manager
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && apt-get install -y ./google-chrome-stable_current_amd64.deb \
    && rm google-chrome-stable_current_amd64.deb \
    #
    && apt clean \
    # Fully purges the lists directory - might be considered unnecessarily aggressive
    && rm -rf /var/lib/apt/lists/* \
    && :

CMD ["python", "main.py"]
