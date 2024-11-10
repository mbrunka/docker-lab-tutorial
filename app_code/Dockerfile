FROM python:3.14.0a1-alpine3.20

# Instalacja git i innych zależności
RUN apk add --no-cache git

RUN python -m ensurepip
RUN pip install --no-cache-dir flask PyYAML flask-healthz requests

WORKDIR /

# Kopiowanie zawartości aplikacji
COPY . .

CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]