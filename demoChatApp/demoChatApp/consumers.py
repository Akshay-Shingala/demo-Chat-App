from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.generics import CreateAPIView
from chatApp.models import PersonalChat,GroupChat,PersonalChatMessage
from asgiref.sync import async_to_sync,sync_to_async
from django.contrib.auth.models import User
# from channels.db import database_sync_to_async
from django.core.serializers import serialize
from chatApp.serializer import PersonalChatMessageSerializer
from django.db.models import Q
import json
class MyPersonalChatWebsocketConsumer(AsyncJsonWebsocketConsumer):
    
    async def connect(self):
        print(type(self.scope['user']))
        print(self.scope['user'])
        if self.scope['user'].is_authenticated:
            resiver=self.scope['url_route']['kwargs']['username']
            print("*****",resiver)              
            if resiver:
                resiver=await database_sync_to_async(User.objects.get)(id=resiver)
                await self.accept()
                chanelId=await self.getOrCreateconnection(self.scope['user'],resiver)
                self.chanelId=chanelId
                temp=json.loads(serialize("json",chanelId))
                self.groupName=str(temp[0]['pk'])
                self.temp=temp     
                print("channel layyer",self.channel_layer)
                await self.channel_layer.group_add(self.groupName,self.channel_name)
                messageDatas=await self.getAllMessages()
                await self.send_json({"messages":messageDatas})
            else:
                await self.accept()
                await self.send(text_data="you not selected your friend")
                await self.close()
        else:
            await self.accept()
            await self.send(text_data="you are not logined")
            await self.close()
        # return await super().connect()

    async def receive(self, text_data=None, bytes_data=None, **kwargs):
        print("Received data", text_data)
        await self.channel_layer.group_send(self.groupName, {
                'type': 'chat.message',
                'message': text_data
            })
        return await super().receive(text_data, bytes_data, **kwargs)
    async def chat_message(self, event):
        print('Event:', event)
        data=await self.saveMessage(event['message'])
    async def disconnect(self, code):
        print('Disconnect:', code)


    @database_sync_to_async
    def getOrCreateconnection(self,sender,resiver):
        chanelId=PersonalChat.objects.filter(Q(sender=sender,resiver=resiver)|Q(sender=resiver,resiver=sender))
        
        if len(chanelId) == 0:
            chanelId=PersonalChat(sender=resiver,resiver=sender)
            chanelId.save()
        return chanelId
        # return await super().disconnect(code)
    


    @database_sync_to_async
    def saveMessage(self,MSG):
        obj=PersonalChat.objects.get(id=int(self.groupName))
        return PersonalChatMessage.objects.create(personalchat=obj,sender=obj.sender,resiver=obj.resiver,message=json.loads(MSG)['text'])
    @database_sync_to_async
    def getAllMessages(self):
        print(self.chanelId[0])
        messages=PersonalChatMessage.objects.filter(personalchat=self.chanelId[0])
        dataSeralizer=PersonalChatMessageSerializer(data=messages,many=True)
        dataSeralizer.is_valid()
        return dataSeralizer.data
 