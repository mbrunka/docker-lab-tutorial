FROM python:3.14.0a1-alpine3.20

# Instalacja git i innych zależności
RUN apk add --no-cache git

RUN python -m ensurepip
RUN pip install --no-cache-dir flask PyYAML flask-healthz requests

WORKDIR /

# Kopiowanie zawartości aplikacji
COPY . .

# Klonowanie repozytorium simple-icons do tymczasowego folderu
# RUN git clone --depth=1 https://github.com/simple-icons/simple-icons.git /tmp/simple-icons

# Skopiowanie tylko zawartości folderu /icons do /app/static/icons
# RUN mkdir -p /app/static/icons && cp -r /tmp/simple-icons/icons/* /app/static/icons/

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]