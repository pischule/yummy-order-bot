# syntax=docker/dockerfile:1

FROM python:3.9-slim

RUN \
apt-get update && \
apt-get install -y apt-transport-https lsb-release curl gnupg && \
echo "deb https://notesalexp.org/tesseract-ocr5/$(lsb_release -cs)/ $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/notesalexp.list > /dev/null && \
curl https://notesalexp.org/debian/alexp_key.asc | apt-key add - && \
apt-get update && \
apt-get install -y gcc libgl1 tesseract-ocr tesseract-ocr-rus

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY app.py app.py
COPY util.py util.py
COPY menu_parser.py menu_parser.py

RUN mkdir -p /app/data

CMD [ "python3", "app.py" ]