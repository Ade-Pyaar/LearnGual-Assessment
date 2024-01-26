import json

from uuid import UUID
from asgiref.sync import async_to_sync

from channels.generic.websocket import WebsocketConsumer

from rest_framework.permissions import IsAuthenticated

from app.models import CustomUser, GroupMessage, Group, models, GroupMembership


class ChatConsumer(WebsocketConsumer):
    permission_class = [IsAuthenticated]

    def connect(self):
        user: CustomUser = self.scope["user"]
        chat_room = f"user_chatroom_{user.id}"

        self.chat_room = chat_room

        async_to_sync(self.channel_layer.group_add)(
            self.chat_room,
            self.channel_name,
        )

        self.accept()

    def receive(self, text_data):
        try:
            received_data: dict = json.loads(text_data)

        except json.decoder.JSONDecodeError:
            return False

        message = received_data.get("message", None)
        sender_id = received_data.get("sender_id")
        receiver_id = received_data.get("receiver_id")
        thread_id = received_data.get("thread_id")

        if not message:
            return False

        sender_user = self.get_user_object(sender_id)
        receiver_user = self.get_user_object(receiver_id)

        thread_obj = self.get_thread(thread_id, sender_user, receiver_user)

        if not all([sender_user, receiver_user, thread_obj]):
            return False

        message_id, message_timestamp = self.create_chat_message(
            thread_obj, sender_user, message, receiver_user
        )

        receiver_chat_room = f"user_chatroom_{receiver_user.id}"

        response = {
            "id": str(message_id),
            "message": message,
            "senderId": str(sender_id),
            "thread_id": str(thread_obj.id),
            "timeStamp": message_timestamp.isoformat(),
            "from": "other",
        }

        async_to_sync(self.channel_layer.group_send)(
            receiver_chat_room,
            {
                "type": "chat_message",
                "message": response,
            },
        )

    def chat_message(self, event):
        message = event["message"]

        self.send(text_data=json.dumps(message))

    def disconnect(self, code):
        pass

    def get_user_object(self, user_id):
        query = CustomUser.objects.filter(id=UUID(user_id))

        if query.exists():
            user = query.first()

        else:
            user = None

        return user

    def get_thread(self, thread_id, sender_user, receiver_user):
        if thread_id is None:
            threads = Group.objects.filter(
                models.Q(sender=sender_user) | models.Q(receiver=sender_user)
            )

            threads = threads.filter(
                models.Q(sender=receiver_user) | models.Q(receiver=receiver_user)
            )

            if threads.exists():
                thread = threads.first()

            else:
                thread = Group()
                thread.receiver = receiver_user
                thread.sender = sender_user
                thread.save()

        else:
            thread = Group.objects.filter(id=UUID(thread_id)).first()

        return thread

    def create_chat_message(self, thread: Group, user: CustomUser, msg: str, receiver: CustomUser):
        message = GroupMessage.objects.create(
            group=thread,
            author=user,
            message=msg,
        )

        receiver_membership = GroupMembership.objects.filter(group=thread, user=receiver).first()

        receiver_membership.unread = True
        receiver_membership.unread_count += 1

        receiver_membership.save()

        return message.id, message.created_at
