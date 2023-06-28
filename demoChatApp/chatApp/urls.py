from django.urls import path,include
from .views import LoginView,RagisterUserAPIView
from .views import UserConsumer
urlpatterns = [
    path('',include('rest_framework.urls')),
    path('LoginUser/',LoginView.as_view(),name="Login"),
    path('ragister/',RagisterUserAPIView.as_view(),name="Ragister"),
    path('usersLists/',UserConsumer.as_asgi(),name="Ragister")
]