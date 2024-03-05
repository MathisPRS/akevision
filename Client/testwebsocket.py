import asyncio
import websockets
import json
import time

async def connect_to_server():
    pc_id = 1  # Remplacez cela par la logique pour obtenir ou générer l'ID du PC
    uri = f"ws://localhost:8000/ws/computer/{pc_id}/"

    async with websockets.connect(uri) as websocket:
        while True:
            message = {"data": {"cpu": 50, "ram": 80, "storage": 60}}
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            print(f"Received from server: {response}")
            
            # Pause de 2 secondes avant d'envoyer la prochaine mise à jour
            await asyncio.sleep(2)

# Appel de la fonction pour établir la connexion
asyncio.get_event_loop().run_until_complete(connect_to_server())
