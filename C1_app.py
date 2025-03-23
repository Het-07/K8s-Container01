from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import requests

app = FastAPI()
PERSISTENT_STORAGE_PATH = "/het_PV_dir"

CONTAINER2_URL = "http://container2-service:8000/compute"

# -----------------------------------------------

# -----------------------------------------------
@app.post("/store-file")
async def store_file(request: Request):
    try:
        data = await request.json()
        filename = data.get("file")
        content = data.get("data")

        if not filename:
            return JSONResponse(status_code=400, content={"file": None, "error": "Invalid JSON input."})

        file_path = os.path.join(PERSISTENT_STORAGE_PATH, filename)
        try:
            with open(file_path, "w") as f:
                f.write(content)
            return {"file": filename, "message": "Success."}
        except:
            return {"file": filename, "error": "Error while storing the file to the storage."}

    except:
        return JSONResponse(status_code=400, content={"file": None, "error": "Invalid JSON input."})

# ----------------------------------------------------------------

# ----------------------------------------------------------------
@app.post("/calculate")
async def calculate(request: Request):
    try:
        data = await request.json()
        filename = data.get("file")
        product = data.get("product")

        if not filename or not product:
            return JSONResponse(status_code=400, content={"file": None, "error": "Invalid JSON input."})

        file_path = os.path.join(PERSISTENT_STORAGE_PATH, filename)

        if not os.path.exists(file_path):
            return JSONResponse(status_code=404, content={"file": filename, "error": "File not found."})

        try:
            response = requests.post(CONTAINER2_URL, json={"file": filename, "product": product})
            response.raise_for_status()
            return JSONResponse(status_code=response.status_code, content=response.json())
        except requests.exceptions.HTTPError as err:
            return JSONResponse(status_code=response.status_code, content=response.json())
        except Exception:
            return JSONResponse(status_code=500, content={"file": filename, "error": "Internal Server Error."})
    except:
        return JSONResponse(status_code=400, content={"file": None, "error": "Invalid JSON input."})
