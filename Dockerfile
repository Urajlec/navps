FROM python:3.12-slim

WORKDIR /app

RUN apt update && apt install -y build-essential libpq-dev

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "photographer_portfolio.wsgi:application", "--bind", "0.0.0.0:8000"]
