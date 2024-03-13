import websockets
import json
import asyncio
import time

# Charger les variables de configuration à partir d'un fichier
with open('config.json') as f:
    config = json.load(f)

# Définir l'URL de la connexion WebSocket avec le token dans l'URL
url = f'ws://{config["server_url"]}/ws/client/{config["client_id"]}/{config["token"]}/'

# Définir les données à envoyer au serveur
data = {
    'data': 'Hello, server!'
}

# Fonction pour envoyer les données au serveur via WebSocket
async def send_data(websocket):
    await websocket.send(json.dumps(data))
    response = await websocket.recv()
    print(f'Réponse du serveur : {response}')

# Fonction pour établir la connexion WebSocket et envoyer les données
async def main():
    async with websockets.connect(url) as websocket:
        while True:
            await send_data(websocket)
            # Attendre 5 secondes avant d'envoyer les données suivantes
            await asyncio.sleep(5)

# Exécuter la fonction principale
asyncio.run(main())
