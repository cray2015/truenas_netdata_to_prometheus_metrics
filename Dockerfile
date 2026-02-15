FROM python:3.11-slim

WORKDIR /app

RUN useradd -u 10001 appuser

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

USER appuser

EXPOSE 9101

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9101"]