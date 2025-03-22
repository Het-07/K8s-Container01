from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os
import requests

app = FastAPI()
PERSISTENT_STORAGE_PATH = "/het_PV_dir"

CONTAINER2_URL = "http://container2-service:8000/compute"

@app.post("/store-file")
async def store_file(request: Request):
    try:
        data = await request.json()
        filename = data.get("file")
        filedata = data.get("data")

        if not filename:
            return JSONResponse(status_code=400, content={"file": None, "error": "Invalid JSON input."})

        file_path = os.path.join(PERSISTENT_STORAGE_PATH, filename)

        try:
            with open(file_path, "w") as f:
                f.write(filedata)
            return {"file": filename, "message": "Success."} 
        except:
            return {"file": filename, "error": "Error while storing the file to the storage."}

    except:
        return JSONResponse(status_code=400, content={"file": None, "error": "Invalid JSON input."})


@app.post("/calculate")
def calculate(data: dict):
    if "file" not in data or not data["file"] or "product" not in data or not data["product"]:
        return {"file": None, "error": "Invalid JSON input."}

    file_path = os.path.join(PERSISTENT_STORAGE_PATH, data["file"])

    if not os.path.exists(file_path):
        return {"file": data["file"], "error": "File not found."}

    try:
        response = requests.post(CONTAINER2_URL, json={
            "file": data["file"],
            "product": data["product"]
        })
        return response.json()
    except requests.exceptions.RequestException:
        return {"file": data["file"], "error": "Container 2 unreachable"}
