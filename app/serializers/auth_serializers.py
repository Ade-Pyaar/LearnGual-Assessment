from django.contrib.auth import authenticate
from rest_framework import serializers

from app.models import CustomUser
from app.enum_classes import APIMessages


from app.api_authentication import MyAPIAuthentication


class NormalLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def login(self, request):
        email: str = self.validated_data["email"].lower()
        password = self.validated_data["password"]

        user: CustomUser = authenticate(request, username=email, password=password)

        if user:
            # login successful
            auth_token, auth_exp = MyAPIAuthentication.get_access_token(
                {
                    "user_id": str(user.id),
                }
            )

            data = {
                "auth_token": auth_token,
                "auth_token_exp": auth_exp,
                "refresh_token": MyAPIAuthentication.get_refresh_token(),
                # "user_details": user_data,
                "user_id": str(user.id),
            }

            return data, None

        return None, APIMessages.LOGIN_FAILURE
