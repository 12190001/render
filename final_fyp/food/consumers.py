import json
from channels.generic.websocket import AsyncWebsocketConsumer
from websocket import create_connection
import ssl


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
    # Create an SSL context
        ssl_context = ssl.create_default_context()

        # Set up the secure WebSocket connection
        ws = create_connection('wss://gofoodie-1a86.onrender.com/ws/notifications/', sslopt={"ssl_context": ssl_context})

        # Join the "notification" group
        await self.channel_layer.group_add("notification", self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
    # Leave the "notification" group
        await self.channel_layer.group_discard("notification", self.channel_name)

        # Close the WebSocket connection
        ws.close()


    async def notify_manager(self, event):
    # Send a notification to the manager
        message = event["message"]

        # Send the message over the WebSocket connection
        ws.send(message)

    async def notify_customer(self, event):
        # Send a notification to the customer
        customer = event["customer"]
        status = event["status"]

        # Send the customer and status information over the WebSocket connection
        ws.send(json.dumps({
            "customer": customer,
            "status": status,
        }))

