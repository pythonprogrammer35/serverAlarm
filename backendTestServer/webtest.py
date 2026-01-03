import asyncio
import websockets

async def connect_to_alarm():
    ngrok_id = "5bb8b20eee0b.ngrok-free.app"
    uri = f"wss://{ngrok_id}/ws"
    
    # Custom headers
    headers = {
        "ngrok-skip-browser-warning": "true",
        "Origin": f"https://{ngrok_id}"
    }

    try:
        # CHANGE 'extra_headers' to 'additional_headers'
        async with websockets.connect(uri, additional_headers=headers) as websocket:
            print(f"Connected to {uri}")
            
            await websocket.send("Hello from Python client!")
            
            while True:
                message = await websocket.recv()
                print(f"Server says: {message}")
                
    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(connect_to_alarm())