from django.contrib import admin

from festival.models import Scene, Request, Voice, TimeSlot, SceneSlot

@admin.register(Scene)  
class SceneAdmin(admin.ModelAdmin):  
    pass


@admin.register(Request)  
class RequestAdmin(admin.ModelAdmin):  
    list_display = ('owner', 'name')


@admin.register(Voice)  
class VoiceAdmin(admin.ModelAdmin):
    list_display = ('request_name', 'censor', 'voice')

    def request_name(self, obj):
        return obj.request.name


@admin.register(TimeSlot)  
class TimeSlotAdmin(admin.ModelAdmin):  
    list_display = ('day', 'time')


@admin.register(SceneSlot)  
class SceneSlotAdmin(admin.ModelAdmin):  
    list_display = ('scene', 'timeslot', 'count')
    

