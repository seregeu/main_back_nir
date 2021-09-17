from django.contrib import admin

from app_api.models import AppApi, Download, Comment


class AppApiAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'rating',
                    'image_url',
                    'downloads_amount'
                    )


class DownloadAdmin(admin.ModelAdmin):
    list_display = ('user',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('content',)


admin.site.register(AppApi, AppApiAdmin)
admin.site.register(Download, DownloadAdmin)
admin.site.register(Comment, CommentAdmin)
