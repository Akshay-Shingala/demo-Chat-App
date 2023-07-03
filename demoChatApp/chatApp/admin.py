from django.contrib import admin
from .models import PersonalChat,GroupMessages,PersonalChatMessage,Chat

class PersonalChatMessageAdmin(admin.ModelAdmin):
    list_display=['personalchat','sender','resiver','message','timestamp']
admin.site.register(PersonalChatMessage,PersonalChatMessageAdmin)

class PersonalChatAdmin(admin.ModelAdmin):
    list_display=['id','sender','resiver']
admin.site.register(PersonalChat,PersonalChatAdmin)

class rooms(admin.ModelAdmin):
    list_display=['id','room_name','allowed_users']
admin.site.register(Chat,rooms)