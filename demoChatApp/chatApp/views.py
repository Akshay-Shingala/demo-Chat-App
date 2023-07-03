from django.contrib.auth.models import User
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
    def create(self, request, *args, **kwargs):
        print(request.data)  # Print the request data
        return super().create(request, *args, **kwargs)

class UserConsumer(ListModelMixin,RetrieveModelMixin,GenericAsyncAPIConsumer):
    queryset=User.objects.all()
    serializer_class=userListSeralizer


def loginPage(request,s=None):
    return TemplateResponse(request,"loginRegister.html",{'form':RagisterUserSerializer})

def chatPage(request):
    return TemplateResponse(request,"index.html")

