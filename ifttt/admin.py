from django.contrib import admin

# Register your models here.
from ifttt.models import Clause, Event


class ClauseAdmin(admin.ModelAdmin):
    pass


class EventAdmin(admin.ModelAdmin):
    pass


class TriggerAdmin(admin.ModelAdmin):
    pass


admin.site.register(Clause, ClauseAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Trigger, TriggerAdmin)
