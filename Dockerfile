FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY README.md .
COPY src ./src

RUN pip install --upgrade pip

RUN pip install torch \
  --index-url https://download.pytorch.org/whl/cpu

RUN pip install .

EXPOSE 8000

CMD ["uvicorn", "article_discovery.api.main:app", "--host", "0.0.0.0", "--port", "8000"]