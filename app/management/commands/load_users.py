from django.core.management.base import BaseCommand

from app.models import CustomUser, Group, GroupMembership
from app.util_classes import CodeGenerator


class Command(BaseCommand):
    help = "Create dummy user"

    def handle(self, *args, **options):
        try:
            user1 = CustomUser()
            user1.email = "user1@email.com"
            user1.set_password("user1@email.com")
            user1.ws_token = CodeGenerator.generate_ws_token()
            user1.save()

            user2 = CustomUser()
            user2.email = "user2@email.com"
            user2.set_password("user2@email.com")
            user2.ws_token = CodeGenerator.generate_ws_token()
            user2.save()

            # create a new group and group membership for them
            group = Group()
            group.save()

            user1_membership = GroupMembership()
            user1_membership.user = user1
            user1_membership.group = group
            user1_membership.save()

            user2_membership = GroupMembership()
            user2_membership.user = user2
            user2_membership.group = group
            user2_membership.save()

            print("Done creating dummy users")

        except Exception as error:
            print(f"Error when creating dummy users: {error}...")
