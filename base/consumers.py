# base/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer

class BaseConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Logic khi kết nối WebSocket
        self.room_name = "base_room"
        self.room_group_name = f"chat_{self.room_name}"

        # Gia nhập nhóm WebSocket
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Xử lý khi kết nối WebSocket bị ngắt
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Nhận dữ liệu từ WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Gửi thông điệp đến tất cả mọi người trong nhóm
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    # Nhận thông điệp từ nhóm
    async def chat_message(self, event):
        message = event['message']

        # Gửi thông điệp đến WebSocket
        await self.send(text_data=json.dumps({
            'message': message
        }))
