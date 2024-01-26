from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
)
from rest_framework.views import APIView

from drf_yasg.utils import swagger_auto_schema


from app.util_classes import APIResponses
from app.enum_classes import APIMessages


from app.serializers.auth_serializers import NormalLoginSerializer


class NormalLoginView(APIView):
    
    
    @swagger_auto_schema(request_body=NormalLoginSerializer)
    def post(self, request, *args, **kwargs):
        """Endpoint for logging in"""
        
        form = NormalLoginSerializer(data=request.data)

        if form.is_valid():
            data, error = form.login(request=request)

            if error:
                return APIResponses.error_response(
                    status_code=HTTP_401_UNAUTHORIZED, message=error
                )

            return APIResponses.success_response(
                message=APIMessages.LOGIN_SUCCESS, status_code=HTTP_200_OK, data=data
            )

        return APIResponses.error_response(
            status_code=HTTP_400_BAD_REQUEST,
            message=APIMessages.FORM_ERROR,
            errors=form.errors,
        )
