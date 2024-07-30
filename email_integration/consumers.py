import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .email_fetcher import fetch_emails  # Ensure this function is implemented


class EmailConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'status': 'Connected',
        }))

    async def disconnect(self, close_code):
        # Clean up any running tasks if necessary
        pass

    async def start_fetching(self, event):
        await self.send(text_data=json.dumps({
            'status': 'Fetching Started',
        }))

        async for message in fetch_emails():
            await self.send(text_data=json.dumps(message))

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['action'] == 'start_fetching':
            await self.channel_layer.send(
                self.channel_name,
                {
                    'type': 'start_fetching',
                }
            )
