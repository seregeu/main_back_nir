from django.contrib import admin

from actions_api.models import Action


class ActionModelAdmin(admin.ModelAdmin):
    list_display = ('app_id', 'user', 'date', 'action_type', 'data')


admin.site.register(Action, ActionModelAdmin)
# Register your models here.
