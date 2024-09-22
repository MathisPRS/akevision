import asyncio
import websockets
import json
import os
import getpass
import uuid
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "config.json")

def get_computer_info():
    computer_name = os.getenv('COMPUTERNAME')
    username = getpass.getuser()
    domain = os.getenv('USERDOMAIN')
    full_username = f"{domain}\\{username}"
    mac_address = get_mac_address()
    return computer_name, full_username, mac_address

def get_mac_address():
    # Utilise le module uuid pour obtenir l'adresse MAC
    mac_num = hex(uuid.getnode()).replace('0x', '').upper()
    mac = ':'.join(mac_num[i: i + 2] for i in range(0, 11, 2))
    return mac

def encrypt_message(cipher_suite, message):
    encrypted_message = cipher_suite.encrypt(json.dumps(message).encode())
    return encrypted_message.decode()

def decrypt_message(cipher_suite, encrypted_message):
    decrypted_message = cipher_suite.decrypt(encrypted_message.encode()).decode()
    return json.loads(decrypted_message)

async def connect_to_server():
    with open(config_path) as f:
        config = json.load(f)

    # Variables du fichier config
    poste_id = config["poste_id"]
    server_url = config["server_url"]
    uri = f"ws://{server_url}/ws/poste/{poste_id}/"
    token = config["token"]
    aes_key = config["aes_key"].encode()  # Assurez-vous que la clé est encodée en bytes
    cipher_suite = Fernet(aes_key)

    # Données à récupérer
    computer_name, full_username, mac_address = get_computer_info()

    # Ajoutez l'en-tête d'authentification
    headers = {
        "Authorization": token
    }

    async with websockets.connect(uri, extra_headers=headers) as websocket:
        # Attendre le message de test
        response_connection = await websocket.recv()
        decrypted_response_connection = decrypt_message(cipher_suite, response_connection)
        print(f'MESSAGE de reception {decrypted_response_connection}')

        if decrypted_response_connection.get('action') == "request_info":
            print('OK pour INFO')
            message_send_info = {
                'action': 'send_info',
                'computer_name': computer_name,
                'full_username': full_username,
                'mac_address': mac_address
            }

        elif decrypted_response_connection.get('action') == "request_mac":
            print('OK pour MAC')
            message_send_info = {
                'action': 'send_mac',
                'mac_address': mac_address
            }

        encrypted_message_send_info = encrypt_message(cipher_suite, message_send_info)
        print(encrypted_message_send_info)
        await websocket.send(encrypted_message_send_info)

        while True:
            message = {
                'action': 'get_info',
                'computer_name': computer_name,
                'full_username': full_username,
                'mac_address': mac_address
            }
            encrypted_message = encrypt_message(cipher_suite, message)
            print(f'Message encrypted: {encrypted_message}')

            await websocket.send(encrypted_message)

            # Recevoir la réponse du serveur
            response = await websocket.recv()
            decrypted_response = decrypt_message(cipher_suite, response)
            print(f"Received from server: {decrypted_response}")

            # Pause de 5 secondes avant d'envoyer la prochaine mise à jour
            await asyncio.sleep(20)

# Appel de la fonction pour établir la connexion
asyncio.get_event_loop().run_until_complete(connect_to_server())
