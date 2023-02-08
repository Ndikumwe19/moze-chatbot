FROM python:3.10.8

#
WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-b 127.0.0.1:8000", "app:app"]