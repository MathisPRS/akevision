import asyncio
import websockets
import json
import time

async def connect_to_server():
    pc_id = 4  # Remplacez cela par la logique pour obtenir ou générer l'ID du PC
    uri = f"ws://localhost:8000/ws/client/{pc_id}/"
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJjbGllbnRfaWQiOjQsImV4cCI6MTcxMTEwMjYyMX0.TAXEoZjRqRPr7f29lmxr_fBPMEV6GZfwa89qdA2fn14'

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
