from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from simple_history.admin import SimpleHistoryAdmin
from .models import *


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_superuser', 'is_active')


class FilesAdmin(SimpleHistoryAdmin):
    list_display = ('file', 'provider', 'date_upload')
    search_fields = ('file',)
    list_display_links = ('file',)


class NumbersAdmin(SimpleHistoryAdmin):
    list_display = ('number', 'attachment', 'comment', 'cf', 'is_enabled')
    search_fields = ('number',)
    list_display_links = ('number',)


class ParserAdmin(SimpleHistoryAdmin):
    list_display = ('number','attachment', 'provider', 'file', 'date_upload', 'payment', 'result_pay')
    search_fields = ('number',)
    list_display_links = ('number',)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Files, FilesAdmin)
admin.site.register(Numbers, NumbersAdmin)
admin.site.register(Parser, ParserAdmin)
admin.site.register(Providers, SimpleHistoryAdmin)
admin.site.register(Attachments, SimpleHistoryAdmin)
admin.site.register(SubscriptionFee, SimpleHistoryAdmin)