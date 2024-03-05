from django.db import models
import random
import string

class Compagnie(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Client(models.Model):
    name = models.CharField(max_length=255, default=None)
    compagnie = models.ForeignKey(Compagnie, on_delete=models.CASCADE, default=None)
    security_key = models.CharField(max_length=32, unique=True)
    installation_script = models.TextField(blank=True)

    def save(self, *args, **kwargs):
        if not self.security_key:
            self.security_key = ''.join(random.choices(string.ascii_letters + string.digits, k=32))
        super().save(*args, **kwargs)

    def generate_script(self):
        script_content = f"""
import asyncio
import websockets
import json
import time

async def connect_to_server():
    pc_id = {self.id}
    security_key = "{self.security_key}"
    uri = f"ws://localhost:8000/ws/computer/{pc_id}/"

    async with websockets.connect(uri) as websocket:
        while True:
            message = {{"cpu": 50, "ram": 80, "storage": 60}}
            await websocket.send(json.dumps(message))
            response = await websocket.recv()
            print(f"Received from server: {response}")
            await asyncio.sleep(2)

asyncio.get_event_loop().run_until_complete(connect_to_server())
"""
        self.installation_script = script_content
        self.save()