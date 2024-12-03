import asyncio
import websockets

"""
WebSocket client for testing purposes
"""

async def websocket_client():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        print("connected")
        while True:
            response = await websocket.recv()
            print(f"Received: {response}")

asyncio.run(websocket_client())
