from django.contrib import admin
from .models import PersonalChat,GroupMessages,PersonalChatMessage

class PersonalChatMessageAdmin(admin.ModelAdmin):
    list_display=['personalchat','sender','resiver','message','timestamp']
admin.site.register(PersonalChatMessage,PersonalChatMessageAdmin)

class PersonalChatAdmin(admin.ModelAdmin):
    list_display=['id','sender','resiver']
admin.site.register(PersonalChat,PersonalChatAdmin)