from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user',
                    'cards',
                    'gender',
                    'second_mail',
                    'phone',
                    'img_url')
    search_fields = ('user__username',)


admin.site.register(UserProfile, UserProfileAdmin)
