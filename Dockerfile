FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .
COPY xgboost-model.pkl .

EXPOSE 7860

CMD ["python", "app.py"]