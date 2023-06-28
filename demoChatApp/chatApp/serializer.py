from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from rest_framework.fields import empty
from .models import *
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields =['username', 'password']

class RagisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username', 'password', 'email', 'first_name', 'last_name']
    def create(self, validated_data):
        
        validated_data['password']=make_password(validated_data['password'])
        return super().create(validated_data)

class UserNameSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields =['username']
    
class PersonalChatMessageSerializer(serializers.ModelSerializer):
    sender=UserNameSerializer(read_only=True)
    resiver=UserNameSerializer(read_only=True)
    class Meta:
        model=PersonalChatMessage
        fields=['personalchat','sender','resiver','message']
    # def __init__(self, instance=None, data=..., **kwargs):
    #     # print("******************",instance, 'instance',list(data),kwargs)
    #     # instance['personalchat']=PersonalChat.objects.get(id=instance['personalchat'])
    #     # instance['sender']=User.objects.get(id=instance['sender'])
    #     # instance['resiver']=User.objects.get(id=instance['resiver'])
    #     # ellipsis
    #     print("upgrade save data",instance, 'instance',data,kwargs)
    #     super().__init__(instance, data, **kwargs)
    
    # def is_valid(self, *, raise_exception=False):
    #     # print (self.context)
    #     return super().is_valid(raise_exception=raise_exception)
    # def create(self, validated_data):
    #     print(validated_data)
    #     # validated_data['personalchat']=PersonalChat.objects.get(id=validated_data['personalchat'])
    #     # validated_data['sender']=User.objects.get(id=validated_data['sender'])
    #     # validated_data['resiver']=User.objects.get(id=validated_data['resiver']) 
    #     return super().create(validated_data)
class userListSeralizer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['id','username','email', 'first_name', 'last_name'] 