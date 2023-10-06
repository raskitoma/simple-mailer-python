FROM python:3.9-slim-buster
ENV FLASK_APP=wsgi.py

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 3001

CMD ["flask", "run", "--host=0.0.0.0", "--port=3001"]	

