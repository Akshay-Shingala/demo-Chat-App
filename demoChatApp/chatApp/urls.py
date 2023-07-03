from django.urls import path,include
from .views import LoginView,RagisterUserAPIView
from .views import UserConsumer,loginPage,chatPage,video,logoutview
urlpatterns = [
    path('LoginUser/',LoginView.as_view(),name="Login"),
    path('ragister/',RagisterUserAPIView.as_view(),name="Ragister"),
    path('usersLists/',UserConsumer.as_asgi(),name="Ragister"),
    path('',include('rest_framework.urls')),
    path('',loginPage,name="LoginPage"),
    path('logoutview/',logoutview,name="logoutview"),
    # path('login/<str:s>',loginPage,name="LoginPage"),
    path('chat/',chatPage,name="chatPage"),
    path('video/<str:room>/',video,name='video'),
    
]