import asyncio
import websockets
import json
import os, time

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "config.json")


async def connect_to_server():
    with open(config_path) as f:
        config = json.load(f)

    pc_id = config["client_id"]
    server_url = config["server_url"]
    uri = f"ws://{server_url}/ws/client/{pc_id}/"
    token = config["token"]

    # Ajoutez l'en-tête d'authentification
    headers = {
        "Authorization": token
    }

    async with websockets.connect(uri, extra_headers=headers) as websocket:
        while True:
            message = {'ram' : 60, 'cpu' : 20, 'test' : 'test'}
            await websocket.send(json.dumps(message))

            response = await websocket.recv()
            print(f"Received from server: {response}")

            # Pause de 2 secondes avant d'envoyer la prochaine mise à jour
            await asyncio.sleep(5)

# Appel de la fonction pour établir la connexion
asyncio.get_event_loop().run_until_complete(connect_to_server())
