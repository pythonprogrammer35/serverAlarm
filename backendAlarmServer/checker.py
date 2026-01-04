from fastapi import FastAPI, WebSocket
import requests
import json
import time
from typing import List
import keyboard
from pynput import keyboard

def on_press(key):
    try:
        if key.char == 'q': # Stop alarm if 'q' is pressed
            print("Quitting...")
            exit()
            return False # Stops the listener
    except AttributeError:
        pass

# Start the listener in a non-blocking way
#listener = keyboard.Listener(on_press=on_press)
#listener.start()

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
    
    await websocket.send_text("Welcome to the server!")
    while controlChecker == False:
        print("jab")
        controlChecker = True
        try:
            print("teep")
            data = await websocket.receive_text()
            print(data)
            await websocket.send_text(f"Recieved message{data}")
            print("step")
            
        except Exception:
            pass
        finally:
            #manager.disconnect(websocket)
            pass
    #manager.disconnect(websocket)
    await check_server_run(websocket)
async def check_server(websocket: WebSocket):
    url = ""

    response = requests.get(url)

    if(response.ok):
        pass
        print("connection successful")
    else:
        #websocket code here
        print("problem occured")
        await websocket.send_text("Warning, server offline")
        print("recieved?")
        
async def check_server_run(websocket: WebSocket):
    print("testing")
    print(controlChecker)
    while controlChecker == True:
        
        print("running")
        await check_server(websocket)
        #waits for 10 minutes
        time.sleep(6)
