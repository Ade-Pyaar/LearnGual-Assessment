import logging

from urllib.parse import parse_qs

import traceback

import jwt

from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR

from channels.db import database_sync_to_async

from django.http import JsonResponse
from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


from app.models import CustomUser


logger = logging.getLogger("server_error")


class Log500ErrorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        logger.error(
            "\n".join(
                traceback.format_exception(type(exception), exception, exception.__traceback__)
            )
        )

        return JsonResponse(
            {
                "responseCode": "99",
                "success": False,
                "message": "An error has occurred but don't worry. We will worry about it",
                "errors": None,
            },
            status=HTTP_500_INTERNAL_SERVER_ERROR,
        )


@database_sync_to_async
def return_user(user_id):
    try:
        user = CustomUser.objects.get(id=user_id)

    except Exception as error:
        print(f"Error inside the middleware: {error}")
        user = AnonymousUser()

    return user


class TokenAuthMiddleWare:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        query_string = scope["query_string"]
        query_params = query_string.decode()
        query_dict = parse_qs(query_params)

        token = query_dict["wstoken"][0]

        try:
            decoded = jwt.decode(token, settings.SECRET_KEY, algorithms="HS256")

        except Exception:
            return None

        exp = decoded["exp"]

        if timezone.now().timestamp() > exp:
            return None

        user = await return_user(decoded["user_id"])

        scope["user"] = user
        return await self.app(scope, receive, send)
