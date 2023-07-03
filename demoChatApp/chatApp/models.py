from django.db import models
from django.contrib.auth.models import User

class PersonalChat(models.Model):
    class Meta:
        unique_together = (('sender', 'resiver'),)
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="sender")
    resiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name="resiver")

    def __str__(self) -> str:
        return self.sender.username + "-" +self.resiver.username 
class GroupChat(models.Model):
    name=models.CharField(max_length=150)

class PersonalChatMessage(models.Model):
    personalchat=models.ForeignKey(PersonalChat,on_delete=models.CASCADE)#models.OneToOneField(User,models.CASCADE) #
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="senderMeaage")
    resiver=models.ForeignKey(User,on_delete=models.CASCADE,related_name="resiverMeaage")
    message=models.TextField()
    timestamp=models.DateTimeField(auto_now_add=True)

class GroupMessages(models.Model):
    sender=models.ForeignKey(User,on_delete=models.CASCADE,related_name="senderGroupMessages")
    message=models.TextField()
    group=models.ForeignKey(GroupChat,verbose_name="group name",on_delete=models.CASCADE)
    timestamp=models.DateTimeField(auto_now_add=True)
    
class Chat(models.Model):
    room_name = models.CharField(max_length=255)
    allowed_users = models.CharField(max_length=255)
  