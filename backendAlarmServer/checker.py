from fastapi import FastAPI, WebSocket
import requests
import json
import time
from typing import List

app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
    
    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
    
    async def broadcast(self, message: dict):
        await self.active_connections[0].send_json(message)
        
    def seeConnection(self):
        return self.active_connections

manager = ConnectionManager()
controlChecker = False

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    global controlChecker
    await manager.connect(websocket)
    while controlChecker == False:
        print("jab")
        controlChecker = True
        try:
            print("teep")
            data = await websocket.receive_text()
            await websocket.send_text(f"Recieved message{data}")
            print("step")
            
        except Exception:
            pass
        finally:
            #manager.disconnect(websocket)
            pass

def check_server():
    url = "https://felisha-dorsoventral-shaly.ngrok-free.dev/normal/"

    response = requests.get(url)

    if(response.ok):
        pass
        print("connection successful")
    else:
        #webhook code here
        print("problem occured")


        pass

while controlChecker == True:
    check_server()
    #waits for 10 minutes
    time.sleep(6)