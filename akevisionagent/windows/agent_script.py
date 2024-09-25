import asyncio
import websockets
import json
import os
import getpass
import uuid
import psutil
from cryptography.fernet import Fernet

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(BASE_DIR, "config.json")

def get_computer_info():
    computer_name = os.getenv('COMPUTERNAME')
    username = getpass.getuser()
    domain = os.getenv('USERDOMAIN')
    full_username = f"{domain}\{username}"
    mac_address = get_mac_address()
    ram_usage = psutil.virtual_memory().percent
    cpu_usage = psutil.cpu_percent(interval=1)

    return computer_name, full_username, mac_address, ram_usage, cpu_usage

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

async def handle_request_token(websocket, cipher_suite, compagnie_token, mac_address):
    print('OK pour TOKEN')
    message_send_token = {
        'action': 'get_token',
        'compagnie_token': compagnie_token,
        'mac_address': mac_address
    }

    encrypted_message_send_token = encrypt_message(cipher_suite, message_send_token)
    print(encrypted_message_send_token)
    await websocket.send(encrypted_message_send_token)

async def handle_update_agent():
    while True:
        print('Salut')
        await asyncio.sleep(10)

async def handle_request_info(websocket, cipher_suite):
    computer_name, full_username, mac_address, ram_usage, cpu_usage = get_computer_info()
    message = {
        'action': 'get_info',
        'computer_name': computer_name,
        'full_username': full_username,
        'mac_address': mac_address,
        'ram_usage': ram_usage,
        'cpu_usage': cpu_usage
    }

    encrypted_message = encrypt_message(cipher_suite, message)
    print(f'Message encrypted: {encrypted_message}')

    await websocket.send(encrypted_message)

async def connect_to_server():
    with open(config_path) as f:
        config = json.load(f)

    # Variables du fichier config
    version_agent = config["version_agent"]
    poste_id = config["poste_id"]
    server_url = config["server_url"]
    uri = f"ws://{server_url}/ws/poste/{poste_id}/"
    token = config["token"]
    compagnie_token = config["compagnie_token"]
    aes_key = config["aes_key"].encode()  # Assurez-vous que la clé est encodée en bytes
    cipher_suite = Fernet(aes_key)

    # Données à récupérer
    computer_name, full_username, mac_address, ram_usage, cpu_usage = get_computer_info()

    # Ajoutez l'en-tête d'authentification
    headers = {
        "Authorization": token,
        "Version": version_agent,
    }

    async with websockets.connect(uri, extra_headers=headers) as websocket:
        # Attendre le message de test
        response_connection = await websocket.recv()
        decrypted_response_connection = decrypt_message(cipher_suite, response_connection)
        print(f'MESSAGE de reception {decrypted_response_connection}')

        # Mapper les actions aux fonctions correspondantes
        handlers = {
            'request_token': lambda: handle_request_token(websocket, cipher_suite, compagnie_token, mac_address),
            'update_agent': handle_update_agent,
            'request_info': lambda: handle_request_info(websocket, cipher_suite),
        }

        # Exécuter la fonction correspondante à l'action reçue
        action = decrypted_response_connection.get('action')
        handler = handlers.get(action)
        if handler:
            await handler()
        else:
            print(f'Action inconnue: {action}')

        # Boucle principale pour écouter les messages du serveur
        while True:
            response = await websocket.recv()
            decrypted_response = decrypt_message(cipher_suite, response)
            print(f"Received from server: {decrypted_response}")

            action = decrypted_response.get('action')
            handler = handlers.get(action)
            if handler:
                await handler()
            else:
                print(f'Action inconnue: {action}')

            # Pause de 7 secondes avant d'envoyer la prochaine mise à jour
            await asyncio.sleep(7)

# Appel de la fonction pour établir la connexion
asyncio.get_event_loop().run_until_complete(connect_to_server())
