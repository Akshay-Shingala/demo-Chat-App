from chatApp.views import UserConsumer
from django.urls import path
from .consumers import MyPersonalChatWebsocketConsumer
# from .consumers import MyGroupChatWebsocketConsumer,MyPersonalChatWebsocketConsumer
WebSocketUrls=[
    path('Personal/<str:username>',MyPersonalChatWebsocketConsumer.as_asgi()),
    # path('Group/<str:username>',MyGroupChatWebsocketConsumer.as_asgi())
    path('usersLists/',UserConsumer.as_asgi(),name="Ragister")
]