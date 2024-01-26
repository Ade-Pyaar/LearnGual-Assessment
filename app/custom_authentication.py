from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CustomAuthenticationBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user_model = get_user_model()

        user = user_model.objects.filter(email=username.lower()).first()

        if user:
            if user.check_password(password):
                return user

            return None

        return None
