from django.urls import path

from app.views.auth_views import NormalLoginView
from app.views.chat_views import ThreadsHomeView, ThreadsSingleView
from app.views.template_views import template_login


urlpatterns = [
    ################################################# auth paths ###################################
    path(
        "auth/login/",
        NormalLoginView.as_view(),
        name="login",
    ),
    ########################################### chat paths ############################################
    path("chats/", ThreadsHomeView.as_view(), name="chat-home"),
    path("chats/<slug:thread_id>/", ThreadsSingleView.as_view(), name="chat-single"),
    ########################################### template paths ############################################
    path("", template_login, name="all-chat-home"),
    # path("chat/<slug:thread_id>/", ThreadsSingleView.as_view(), name="chat-single"),
]
