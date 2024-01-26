from uuid import UUID

from django.conf import settings
from django.db.models import Q


from rest_framework import serializers


from app.models import GroupMembership, GroupMessage, Group, CustomUser


class ChatMessageSerializer(serializers.Serializer):
    def to_representation(self, instance: GroupMessage):
        current_user: CustomUser = self.context.get("current_user")

        # last_read_message: GroupMessage = self.context.get("last_read_message")
        other_user: GroupMembership = self.context.get("other_user")

        data = {}
        data["id"] = instance.id
        data["content"] = instance.message
        data["sender_id"] = instance.author.id
        data["date_created"] = instance.timestamp.strftime("%Y-%m-%d %H:%M")
        data["sender"] = instance.author == current_user

        if instance.author != other_user.user:
            if other_user.last_read_message:
                data["read"] = instance.timestamp <= other_user.last_read_message.timestamp

            else:
                data["read"] = False

        return data


class ThreadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["id", "timestamp", "unread", "unread_count"]

    def to_representation(self, instance: Group):
        data = super().to_representation(instance)

        current_user: CustomUser = self.context.get("current_user")

        if current_user == instance.receiver:
            receiver_data = {
                "id": instance.sender.id,
                "name": instance.sender.name,
                "picture": instance.sender.picture.url
                if instance.sender.picture
                else settings.DEFAULT_PROFILE_PICTURE,
            }

        else:
            receiver_data = {
                "id": instance.receiver.id,
                "name": instance.receiver.name,
                "picture": instance.receiver.picture.url
                if instance.receiver.picture
                else settings.DEFAULT_PROFILE_PICTURE,
            }

        try:
            last_message = instance.chatmessage_thread.latest("timestamp")

        except GroupMessage.DoesNotExist:
            last_message = None

        last_message_data = ChatMessageSerializer(
            last_message,
            context={
                "current_user": current_user,
                "last_read_message": last_message,
                # "other_user": other_user,
            },
        ).data

        data["receiver_data"] = receiver_data
        data["last_message"] = last_message_data

        return data


class ThreadNewSerializer(serializers.Serializer):
    sender_id = serializers.UUIDField()
    receiver_id = serializers.UUIDField()

    def validate(self, attrs):
        data = super().validate(attrs)

        sender_id = data["sender_id"]
        receiver_id = data["receiver_id"]

        try:
            sender_user = CustomUser.objects.get(id=sender_id)

        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"sender_id": "Invalid sender"})

        try:
            receiver_user = CustomUser.objects.get(id=receiver_id)

        except CustomUser.DoesNotExist:
            raise serializers.ValidationError({"receiver_id": "Invalid sender"})

        lookup1 = Q(sender=sender_user) & Q(receiver=receiver_user)
        lookup2 = Q(sender=receiver_user) & Q(receiver=sender_user)
        lookup = Q(lookup1 | lookup2)
        threads = Group.objects.filter(lookup)
        if threads.exists():
            raise serializers.ValidationError(
                {
                    "sender_id": f"Thread between {sender_user.name} and {receiver_user.name} already exists."
                }
            )

        return data

    def create_thread(self):
        sender_id = self.validated_data["sender_id"]
        receiver_id = self.validated_data["receiver_id"]

        sender_user = CustomUser.objects.get(id=sender_id)
        receiver_user = CustomUser.objects.get(id=receiver_id)

        new_thread = Group()
        new_thread.sender = sender_user
        new_thread.receiver = receiver_user
        new_thread.save()

        thread_data = {
            "id": new_thread.id,
            "timestamp": new_thread.timestamp,
            "receiver_data": {
                "id": new_thread.receiver.id,
                "name": new_thread.receiver.name,
                "picture": new_thread.receiver.picture.url
                if new_thread.receiver.picture
                else settings.DEFAULT_PROFILE_PICTURE,
            },
        }

        return thread_data


class GroupMembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMembership
        fields = ["id"]

    def to_representation(self, instance: GroupMembership):
        data = super().to_representation(instance)

        user: CustomUser = self.context.get("current_user")

        # get the other user in the group
        other_user: GroupMembership = instance.group.group_members.exclude(user=user).first()

        if instance.last_read_message:
            time = instance.last_read_message.created_at.strftime("%Y-%m-%d %H:%M")
        else:
            time = ""

        data = {
            "id": instance.group.id,
            "name": other_user.user.email,
            "last_message": ChatMessageSerializer(
                instance.last_read_message,
                context={
                    "current_user": user,
                    "last_read_message": instance.last_read_message,
                    "other_user": other_user,
                },
            ).data,
            "time": time,
            "unread": instance.unread,
        }
        

        return data


class GetThreadsSerializer(serializers.Serializer):
    @classmethod
    def get_all_threads(cls, request):
        memberships = GroupMembership.objects.filter(user=request.user)

        data = GroupMembershipSerializer(
            memberships, many=True, context={"current_user": request.user}
        ).data

        return data

    @classmethod
    def get_single_thread(cls, thread_id: str, request):
        try:
            thread = Group.objects.filter(id=UUID(thread_id)).first()

        except Exception:
            return None

        if thread is None:
            return None

        return thread

    @classmethod
    def get_single_thread_messages(cls, request, thread: Group):
        try:
            thread_messages = thread.chatmessage_group.all().order_by("created_at")

        except GroupMessage.DoesNotExist:
            thread_messages = None

        # gt group membership

        membership = GroupMembership.objects.filter(user=request.user, group=thread).first()

        other_user: CustomUser = thread.group_members.exclude(user=request.user).first()

        # update the thread read status
        membership.unread = False
        membership.unread_count = 0
        membership.last_read_message = thread_messages.last()
        membership.save()

        if membership.last_read_message:
            time = membership.last_read_message.created_at.strftime("%Y-%m-%d %H:%M")
        else:
            time = ""

        total_data = {
            "name": other_user.user.email,
            "receiver_id": other_user.user.id,
            "id": membership.group.id,
            "time": time,
            "unread": membership.unread,
            "messages": ChatMessageSerializer(
                thread_messages,
                many=True,
                context={
                    "current_user": request.user,
                    "last_read_message": membership.last_read_message,
                    "other_user": other_user,
                },
            ).data,
        }

        return total_data

    @classmethod
    def delete_single_thread(cls, thread: Group):
        thread.delete()

    @classmethod
    def pin_single_thread(cls, thread: Group):
        thread.pinned = True
        thread.save()

    @classmethod
    def unpin_single_thread(cls, thread: Group):
        thread.pinned = False
        thread.save()
