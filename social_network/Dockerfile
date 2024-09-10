FROM python:3.12-slim

WORKDIR /app

COPY social_network/requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "social_network.wsgi:application"]
