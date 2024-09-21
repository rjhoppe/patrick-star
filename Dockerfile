FROM python:3.10
ENV LANG=C.UTF-8

WORKDIR /app

COPY . /app

RUN : \
    && apt-get update \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean \
    # Fully purges the lists directory - might be considered unnecessarily aggressive
    && rm -rf /var/lib/apt/lists/* \
    && :

CMD ["python", "main.py"]
