import json
from channels.generic.websocket import AsyncWebsocketConsumer
import websockets
import ssl


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Create an SSL context
        ssl_context = ssl.create_default_context()

        # Set up the secure WebSocket connection
        self.ws = await websockets.connect('wss://gofoodie-1a86.onrender.com/ws/notifications/', ssl=ssl_context)

        # Join the "notification" group
        await self.channel_layer.group_add("notification", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the "notification" group
        await self.channel_layer.group_discard("notification", self.channel_name)

        # Close the WebSocket connection
        await self.ws.close()

    async def notify_manager(self, event):
        await self.ws.send(json.dumps({
            "type": "notification",
            "message": event["message"],
        }))

    async def notify_customer(self, event):
        await self.ws.send(json.dumps({
            "type": "notification",
            "customer": event["customer"],
            "status": event["status"]
        }))
