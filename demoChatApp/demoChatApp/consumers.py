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
        
        if self.scope['user'].is_authenticated:
            resiver=self.scope['url_route']['kwargs']['username']
                         
            if resiver:
                resiver=await database_sync_to_async(User.objects.get)(id=resiver)
                await self.accept()
                chanelId=await self.getOrCreateconnection(self.scope['user'],resiver)
                self.chanelId=chanelId
                temp=json.loads(serialize("json",chanelId))
                self.groupName=str(temp[0]['pk'])
                self.temp=temp     
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
        
        await self.channel_layer.group_send(self.groupName, {
                'type': 'chat.message',
                'message': text_data,
                'sent': False
            })
        return await super().receive(text_data, bytes_data, **kwargs)
    async def chat_message(self, event):
       
        if not event.get('sent', False):
            event['sent'] = True
            await self.saveMessage(json.loads(event['message']).get('text', None),json.loads(event['message']).get('user', None))
        await self.send_json({'yourmsg':json.loads(event['message']).get('text', None),'user':json.loads(event['message']).get('user', None)})
        # await self.send_json({'yourmsg':json.loads(event['message']).get('data', None),'user':self.scope["user"].username})
    async def disconnect(self, code):
        print('Disconnect:', code)


    @database_sync_to_async
    def saveMessage(self,message,user):
       
        # self.scope['user']
        PCobject=PersonalChat.objects.get(id=self.groupName)
          
        if user==PCobject.sender.id:
            return PersonalChatMessage.objects.create(personalchat=PCobject,sender=PCobject.sender,resiver=PCobject.resiver,message=message)
        else:
            return PersonalChatMessage.objects.create(personalchat=PCobject,sender=PCobject.resiver,resiver=PCobject.sender,message=message)
        # return PersonalChat.objects.get(id=self.groupName)
        # return obj.save()
        # return "sdfdsfdf"
    @database_sync_to_async
    def getOrCreateconnection(self,sender,resiver):
        chanelId=PersonalChat.objects.filter(Q(sender=sender,resiver=resiver)|Q(sender=resiver,resiver=sender))
        
        if len(chanelId) == 0:
            chanelId=PersonalChat(sender=resiver,resiver=sender)
            chanelId.save()
        return chanelId
        # return await super().disconnect(code)
    


    
    @database_sync_to_async
    def getAllMessages(self):
        
        messages=PersonalChatMessage.objects.filter(personalchat=self.chanelId[0])
        dataSeralizer=PersonalChatMessageSerializer(data=messages,many=True)
        dataSeralizer.is_valid()
        return (dataSeralizer.data,{'sessionId': self.scope['user'].id})
 