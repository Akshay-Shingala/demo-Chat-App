from django.urls import path,include
from .views import LoginView,RagisterUserAPIView
from .views import UserConsumer,loginPage,chatPage
urlpatterns = [
    path('LoginUser/',LoginView.as_view(),name="Login"),
    path('ragister/',RagisterUserAPIView.as_view(),name="Ragister"),
    path('usersLists/',UserConsumer.as_asgi(),name="Ragister"),
    path('',loginPage,name="LoginPage"),
    # path('login/<str:s>',loginPage,name="LoginPage"),
    path('chat/',chatPage,name="chatPage"),
    path('',include('rest_framework.urls')),
    
]