FROM python:3.12-slim

WORKDIR /code

RUN apt-get update && apt-get install -y build-essential curl \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY ./src /code/src
COPY .env /code/.env


ENV PYTHONPATH=/code

EXPOSE 80

# Start app
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]
