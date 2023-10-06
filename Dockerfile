FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED=0

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3001

CMD [ "python", "-u", "./app.py" ]
