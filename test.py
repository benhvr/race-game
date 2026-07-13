# test_server.py
import asyncio
import websockets

async def test():
    async with websockets.connect("ws://localhost:8765") as ws:
        # Envoie "avancer" pendant 2 secondes
        await ws.send('{"z": true, "s": false, "q": false, "d": false}')
        for _ in range(5):
            msg = await ws.recv()
            import json
            data = json.loads(msg)
            print("Position voiture :", data["car"]["position"])
            await asyncio.sleep(0.2)

asyncio.run(test())