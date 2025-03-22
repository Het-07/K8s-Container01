# Container - 01
from fastapi import FastAPI, HTTPException
import requests, os

app = FastAPI()
PERSISTENT_STORAGE_PATH = "/het_PV_dir"
os.makedirs(PERSISTENT_STORAGE_PATH, exist_ok=True)

CONTAINER2_URL = "http://container2-service:8000/compute"

@app.post("/store-file")
async def store_file(data: dict):
    if "file" not in data or "data" not in data:
        return {"file": None, "error": "Invalid JSON input."}
    file_path = os.path.join(PERSISTENT_STORAGE_PATH, data["file"])
    try:
        with open(file_path, "w") as f:
            f.write(data["data"])
        return {"file": data["file"], "message": "Success."}
    except:
        return {"file": data["file"], "error": "Error while storing the file to the storage."}

@app.post("/calculate")
async def calculate(data: dict):
    try:
        file_value = data.get("file")

        if not file_value or not isinstance(file_value, str) or file_value.strip() == "":
            return {"file": None, "error": "Invalid JSON input."}

        file_path = os.path.join(PERSISTENT_STORAGE_PATH, file_value)

        if not os.path.exists(file_path):
            return {"file": file_value, "error": "File not found."}

        try:
            response = requests.post(CONTAINER2_URL, json={
                "file": file_value,
                "product": data.get("product", "")
            })
            
            return response.json()
        except requests.exceptions.RequestException:
            return {"file": file_value, "error": "Input file not in CSV format."}

    except Exception as e:
        return {"file": None, "error": "Invalid JSON input."}


