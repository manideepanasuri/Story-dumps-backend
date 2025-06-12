from django.contrib import admin

from .models import *
# Register your models here.

admin.site.register(TaskModel)
admin.site.register(BackGroundModel)
admin.site.register(VoiceModel)