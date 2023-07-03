from django.contrib.auth.models import User
from django.shortcuts import redirect
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import login
from .serializer import UserSerializer,RagisterUserSerializer,PersonalChatMessage,PersonalChat,PersonalChatMessageSerializer,userListSeralizer
from rest_framework.authentication import SessionAuthentication
from django.contrib.auth import authenticate
from rest_framework.generics import *
from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
from djangochannelsrestframework.mixins import  ListModelMixin,RetrieveModelMixin
from django.template.response import TemplateResponse
from django.db.models import Q
from rest_framework import serializers
from .models import Chat
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.messages import constants as messages

class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)
    authentication_classes=[SessionAuthentication]
    serializer_class=UserSerializer
    def get(self, request,formet=None,**kwargs):
        print(request.user)
        # print(self.request.session['user'])
        return Response({'user':''})
    def post(self, request, format=None):
        print(request.POST)
        username=request.POST.get('username',"not found")
        password=request.POST.get("password","not found password")
        print('******************')
        user = authenticate(username=username, password=password)
        if user :
            login(request, user)
            user=UserSerializer(user)
            return Response({'user':user.data}, status=200)
        else:
            return Response({"msg":"username or password is wrong"})

class RagisterUserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RagisterUserSerializer

class UserConsumer(ListModelMixin,RetrieveModelMixin,GenericAsyncAPIConsumer):
    queryset=User.objects.all()
    serializer_class=userListSeralizer


def loginPage(request,s=None):
    return TemplateResponse(request,"loginRegister.html")

def chatPage(request):
    return TemplateResponse(request,"index.html")




def video(request,room,created="created"):
    print(room)
    resiver = User.objects.get(id=room)
    sender = request.user
    chanelId = PersonalChat.objects.filter(Q(sender=sender,resiver=resiver)|Q(sender=resiver,resiver=sender)).first()
    print("*************************",chanelId.id)
    
    get_room = Chat.objects.filter(room_name=chanelId.id)
    if get_room:
        c = get_room[0]
        number = c.allowed_users
        if int(number) < 2:
            number = 2
            c.delete()
            return  TemplateResponse(request,'video.html',{'room':chanelId.id,'created':"join"})
    
    else:
        create = Chat.objects.create(room_name=chanelId.id,allowed_users=1)
        if create:
            return  TemplateResponse(request,'video.html',{'room':chanelId.id,'created':"created"})
    
    # return redirect(reverse('login'))



@login_required
def logoutview(request):
    logout(request)
    # messages.info(request, "Logged out successfully!")
    return redirect("/login/")
