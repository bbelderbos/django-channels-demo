import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.db import transaction

from .models import Message, Ticket


class TicketConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.ticket_id = self.scope['url_route']['kwargs']['ticket_id']
        self.room_group_name = f"ticket_{self.ticket_id}"

        await self.accept()

        # Send previous chat history
        messages = await self.get_chat_history()
        for message in messages:
            print(message)
            await self.send(text_data=json.dumps({
                "message": message.content,
                "sender": message.sender.username,  # Use username for serialization
                "timestamp": message.timestamp.isoformat(),
            }))

        # Join the room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

    async def disconnect(self, close_code):
        # Leave the room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message_content = data['message']
        sender = data['sender']

        # Save message to the database
        await self.save_message(sender, message_content)

        # Broadcast the message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message_content,
                "sender": sender,  # Only broadcast the username
            }
        )

    async def chat_message(self, event):
        # Send the message to WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender": event["sender"],
        }))

    @database_sync_to_async
    def save_message(self, sender, content):
        with transaction.atomic():
            ticket = Ticket.objects.select_for_update().get(id=int(self.ticket_id))
            user = User.objects.get(username=sender)
            Message.objects.create(ticket=ticket, sender=user, content=content)

    @database_sync_to_async
    def get_chat_history(self):
        with transaction.atomic():
            return list(
                Message.objects.filter(ticket_id=int(self.ticket_id))
                .select_related("sender")
                .order_by("timestamp")
            )
