FROM python:3.13-slim
ENV LANG=C.UTF-8

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

# Set env vars
ENV URL=
ENV STORE_PAGE1=
ENV STORE_PAGE2=
ENV STORE_PAGE3=
ENV STORE_PAGE4=
ENV STORE_PAGE5=
ENV NTFY_URL=
ENV WEBHOOK=

# Ensure the cache directory exists
RUN mkdir -p /app/cache

CMD ["python3", "main.py"]
