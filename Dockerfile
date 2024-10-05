FROM infologistix/docker-selenium-python:alpine
ENV LANG=C.UTF-8

WORKDIR /app

COPY . /app

RUN : \
    && pip install --no-cache-dir --ignore-installed -r requirements.txt \
    && :

CMD ["python", "main.py"]
