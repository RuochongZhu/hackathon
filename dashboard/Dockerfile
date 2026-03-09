FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PORT=8080

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY app ./app
COPY dashboard ./dashboard
COPY data ./data
COPY docs ./docs
COPY README.md ./README.md
COPY pytest.ini ./pytest.ini
COPY .env.example ./.env.example

EXPOSE 8080

CMD sh -c "python -m shiny run --host 0.0.0.0 --port ${PORT:-8080} dashboard/ui_app.py"
