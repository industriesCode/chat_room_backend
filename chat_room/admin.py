from django.contrib import admin
from chat_room.models import Room, Messages
# Register your models here.

admin.site.register(Room)
admin.site.register(Messages)
