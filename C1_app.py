from fastapi import FastAPI, HTTPException
import requests
import os

app = FastAPI()

# Persistent storage path in GKE
PERSISTENT_STORAGE_PATH = "/het_PV_dir"

os.makedirs(PERSISTENT_STORAGE_PATH, exist_ok=True)

CONTAINER2_URL = "http://container2-service:8000/compute"  # Kubernetes Service name

@app.post("/store-file")
async def store_file(data: dict):
    """Stores the file data in the persistent volume."""
    if "file" not in data or "data" not in data:
        return {"file": None, "error": "Invalid JSON input."}

    file_path = os.path.join(PERSISTENT_STORAGE_PATH, data["file"])

    try:
        with open(file_path, "w") as f:
            f.write(data["data"])
        return {"file": data["file"], "message": "Success."}
    except Exception as e:
        return {"file": data["file"], "error": str(e)}

@app.post("/calculate")
async def calculate(data: dict):
    """Reads the stored file and sends it to Container 2 for processing."""
    if "file" not in data or not data["file"]:
        return {"file": None, "error": "Invalid JSON input."}

    file_path = os.path.join(PERSISTENT_STORAGE_PATH, data["file"])

    if not os.path.exists(file_path):
        return {"file": data["file"], "error": "File not found."}

    try:
        response = requests.post(CONTAINER2_URL, json={"file": data["file"], "product": data.get("product", "")}, timeout=10)
        response.raise_for_status()  # Ensures proper status code handling
        return response.json()
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=500, detail="Container2 unavailable")
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Container2 timeout")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Container2 Error: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=6000)
