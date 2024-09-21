import asyncio
import websockets
import json
import os, time, getpass
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "config.json")


async def connect_to_server():
    with open(config_path) as f:
        config = json.load(f)

    #Variable du fichier config
    poste_id = config["poste_id"]
    server_url = config["server_url"]
    uri = f"ws://{server_url}/ws/poste/{poste_id}/"
    token = config["token"]
    aes_key = config["aes_key"]
    cipher_suite = Fernet(aes_key)

    #donnée a récup 
    computer_name = os.getenv('COMPUTERNAME')
    username = getpass.getuser()
    domain = os.getenv('USERDOMAIN')
    full_username = f"{domain}\\{username}" 
    

    # Ajoutez l'en-tête d'authentification
    headers = {
        "Authorization": token
    }

    async with websockets.connect(uri, extra_headers=headers) as websocket:
        while True:
            message = {
                'action': 'get_info',
                'computer_name': computer_name,
                'full_username': full_username
                }
            encrypted_message = cipher_suite.encrypt(json.dumps(message).encode())
            encrypted_message_str = encrypted_message.decode()
            print(f'Message encrypter {encrypted_message_str}')

            await websocket.send(encrypted_message_str)

            # encrypted_response = await websocket.recv()
            # response = cipher_suite.decrypt(encrypted_response).decode()
            # response_data = json.loads(response)

            response = await websocket.recv()
            print(f"Received from server: {response}")

            # Pause de 2 secondes avant d'envoyer la prochaine mise à jour
            await asyncio.sleep(5)

# Appel de la fonction pour établir la connexion
asyncio.get_event_loop().run_until_complete(connect_to_server())
