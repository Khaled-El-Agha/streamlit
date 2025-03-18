from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
import subprocess
import shutil

app = FastAPI()

# Serve static files (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve the HTML page
@app.get("/", response_class=HTMLResponse)
def serve_page():
    with open("templates/index.html", "r") as file:
        return file.read()

# API to shutdown STM32MP1
@app.post("/shutdown")
def shutdown():
    os.system("shutdown -h now")
    return JSONResponse(content={"status": "shutting down"})

# API to start or stop the M4 core
@app.post("/m4_core/{action}")
def control_m4(action: str):
    if action == "start":
        subprocess.run(["echo", "Starting M4 Core"])  # Replace with actual command
        return JSONResponse(content={"status": "M4 Core Started"})
    elif action == "stop":
        subprocess.run(["echo", "Stopping M4 Core"])  # Replace with actual command
        return JSONResponse(content={"status": "M4 Core Stopped"})
    return JSONResponse(content={"error": "Invalid action"}, status_code=400)

# API to copy images from USB to SD card
@app.post("/copy_images")
def copy_images():
    src = "/media/usb/images"  # Adjust the path as per your setup
    dest = "/media/sdcard/images"

    if not os.path.exists(src):
        return JSONResponse(content={"error": "USB not found"}, status_code=400)

    if not os.path.exists(dest):
        os.makedirs(dest)

    # Copy files
    for file_name in os.listdir(src):
        shutil.copy(os.path.join(src, file_name), dest)

    return JSONResponse(content={"status": "Copy completed"})


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()