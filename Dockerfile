FROM python:3.8.5-slim-buster

RUN apt-get update \
    && apt-get install -y build-essential pkg-config python-dev \
    --no-install-recommends git \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /opt/app
WORKDIR /opt/app

EXPOSE 8000

ENTRYPOINT ["gunicorn"]
CMD ["-w", "1", "-k", "uvicorn.workers.UvicornWorker", "src.api:app", "--bind", "0.0.0.0:8000"]
