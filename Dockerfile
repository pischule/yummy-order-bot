# syntax=docker/dockerfile:1

FROM pischule/python-opencv-tesseract:latest

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY app.py app.py
COPY util.py util.py
COPY menu_parser.py menu_parser.py

RUN mkdir -p /app/data

CMD [ "python3", "app.py" ]