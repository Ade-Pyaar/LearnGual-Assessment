# import asyncio
# import websockets
# import json

# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi

from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_404_NOT_FOUND,
)


from app.enum_classes import APIMessages
from app.util_classes import APIResponses
from app.serializers.chat_serializers import (
    GetThreadsSerializer,
)


# async def my_async_helper_function(ws_string, message):
#     print(ws_string)

#     try:
#         timeout = 5
#         try:
#             ws_conn = await asyncio.wait_for(websockets.connect(ws_string), timeout)
#         except Exception as error:
#             print(error)
#             return False

#         await ws_conn.send(json.dumps({"type": "whatsapp", "message": message}))
#         # response = await ws_conn.recv()
#         await ws_conn.close()

#         print("done sending, should close now")
#         return True

#     except Exception as e:
#         print(e)
#         await ws_conn.close()
#         return False


class ThreadsHomeView(APIView):
    
    
    permission_classes = [IsAuthenticated]

    
    def get(self, request, *args, **kwargs):
        """Endpoint for getting all chat threads"""

        data = GetThreadsSerializer.get_all_threads(request=request)

        return APIResponses.success_response(
            message=APIMessages.SUCCESS,
            status_code=HTTP_200_OK,
            data=data,
        )


class ThreadsSingleView(APIView):
    permission_classes = [IsAuthenticated]



    
    def get(self, request, thread_id, *args, **kwargs):
        """Endpoint for getting messages inside a chat"""

        thread = GetThreadsSerializer.get_single_thread(thread_id=thread_id, request=request)

        if thread:
            thread_messages = GetThreadsSerializer.get_single_thread_messages(
                request=request, thread=thread
            )

            # TODO send a websocket request to update last read message

            # ws_string = f"ws://{settings.HOST_NAME}/ws/chat/{customer.id}/whatsapp"

            # loop = asyncio.new_event_loop()
            # asyncio.set_event_loop(loop)
            # _ = loop.run_until_complete(
            #     my_async_helper_function(ws_string=ws_string, message=user_message)
            # )

            return APIResponses.success_response(
                message=APIMessages.SUCCESS,
                status_code=HTTP_200_OK,
                data=thread_messages,
            )

        return APIResponses.error_response(
            message=APIMessages.THREAD_NOT_FOUND,
            status_code=HTTP_404_NOT_FOUND,
        )
