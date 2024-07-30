import json
from channels.generic.websocket import AsyncWebsocketConsumer
from .email_fetcher import fetch_emails  # Мы предположим, что эта функция реализована


class EmailConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'status': 'Connected',
        }))

    async def disconnect(self, close_code):
        pass

    async def start_fetching(self, event):
        await self.send(text_data=json.dumps({
            'status': 'Fetching Started',
        }))

        # Здесь мы вызываем функцию fetch_emails, которая будет отправлять обновления прогресса
        reading_messages = True

        async for message in fetch_emails():
            if reading_messages:
                await self.send(text_data=json.dumps({
                    'progress': message['progress'],
                    'subject': message['subject'],
                    'send_date': message['send_date'],
                    'received_date': message['received_date'],
                    'description': message['description'],
                    'status': 'Fetching'
                }))
                if message['progress'] >= 100:
                    reading_messages = False
            await self.send(text_data=json.dumps({
                'progress': message['progress'],
                'subject': message['subject'],
                'status': 'Processing'
            }))

        await self.send(text_data=json.dumps({
            'status': 'Completed',
        }))

    async def receive(self, text_data):
        data = json.loads(text_data)
        if data['action'] == 'start_fetching':
            await self.channel_layer.send(
                self.channel_name,
                {
                    'type': 'start_fetching',
                }
            )