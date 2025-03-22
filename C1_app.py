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
    if "file" not in data:
        return {"file": None, "error": "Invalid JSON input."}

    file_path = os.path.join(PERSISTENT_STORAGE_PATH, data["file"])

    if not os.path.exists(file_path):
        return {"file": data["file"], "error": "File not found."}

    try:
        with open(file_path, "r") as f:
            reader = csv.reader(f)
            headers = next(reader)
            headers = [h.strip().lower() for h in headers]
            if "product" not in headers or "amount" not in headers:
                return {"file": data["file"], "error": "Input file not in CSV format."}
    except:
        return {"file": data["file"], "error": "Input file not in CSV format."}

    try:
        response = requests.post(CONTAINER2_URL, json={
            "file": data["file"],
            "product": data.get("product", "")
        })
        return response.json()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="Container 2 unreachable")


