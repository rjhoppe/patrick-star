FROM python:3.12-slim
ENV LANG=C.UTF-8

ARG URL
ARG STORE_PAGE1
ARG STORE_PAGE2
ARG STORE_PAGE3
ARG STORE_PAGE4
ARG STORE_PAGE5

# Set environment variables from arguments
ENV URL=${URL}
ENV STORE_PAGE1=${STORE_PAGE1}
ENV STORE_PAGE2=${STORE_PAGE2}
ENV STORE_PAGE3=${STORE_PAGE3}
ENV STORE_PAGE4=${STORE_PAGE4}
ENV STORE_PAGE5=${STORE_PAGE5}

WORKDIR /app

COPY . /app

RUN : \
  && apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y \
  wget \
  unzip \
  libxss1 \
  libappindicator3-1 \
  libatk-bridge2.0-0 \
  libgtk-3-0 \
  libnspr4 \
  libnss3 \
  libx11-xcb1 \
  libxcomposite1 \
  libxrandr2 \
  libxcursor1 \
  libxi6 \
  libxtst6 \
  libasound2 \
  fonts-liberation \
  libgbm1 \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/* \
  && :

RUN : \
  && pip install --no-cache-dir --ignore-installed -r requirements.txt \
  && :

CMD ["python3", "main.py"]
