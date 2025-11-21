import uvicorn
import json
import cv2
import numpy as np
import base64

from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from rt_llama.smbnv_client import image_response

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            # The data is a base64 encoded image URL, so we need to remove the prefix
            image_base64 = data.split(',')[1]

            # Decode base64 image
            nparr = np.frombuffer(base64.b64decode(image_base64), np.uint8)
            frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            # Resize the frame to 640x480
            resized_frame = cv2.resize(frame, (640, 480))

            # Encode the resized frame back to base64
            _, buffer = cv2.imencode('.jpg', resized_frame)
            resized_image_base64 = base64.b64encode(buffer).decode('utf-8')
            
            description, yoshi_found = image_response(resized_image_base64)
            response = {"description": description, "yoshi_found": yoshi_found}
            await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"An error occurred: {e}")
        await websocket.close(code=1011)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
