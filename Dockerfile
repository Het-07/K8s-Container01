FROM python:3.9-slim
WORKDIR /app

# Copy application files first (to avoid caching old versions)
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Ensure PV directory exists
RUN mkdir -p /het_PV_dir

CMD ["uvicorn", "C1_app:app", "--host", "0.0.0.0", "--port", "6000"]
