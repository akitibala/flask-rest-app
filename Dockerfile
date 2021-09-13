FROM python:3.8-slim-buster

WORKDIR /app
EXPOSE 8000

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "app.py"]