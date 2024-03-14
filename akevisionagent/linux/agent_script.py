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

# Fonction pour mettre à jour le token dans le fichier de configuration
def update_token(new_token):
    with open('config.json', 'w') as f:
        config['token'] = new_token
        json.dump(config, f)

# Exécuter la fonction principale
try:
    asyncio.run(main())
except websockets.exceptions.ConnectionClosedError as e:
    # Vérifier si le serveur a fermé la connexion en raison d'un token expiré
    if e.code == 1008:
        # Appeler une fonction pour obtenir un nouveau token et mettre à jour le fichier de configuration
        new_token = get_new_token()
        update_token(new_token)
        # Réessayer de se connecter au serveur avec le nouveau token
        asyncio.run(main())
    else:
        print(f'Erreur de connexion : {e}')
