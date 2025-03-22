FROM python:3.9-slim
WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN mkdir -p /het_PV_dir

CMD ["uvicorn", "C1_app:app", "--host", "0.0.0.0", "--port", "6000"]
