from django.contrib import admin
from django.contrib import admin
from .models import ChatHistory

# Register the ChatHistory model
@admin.register(ChatHistory)
class ChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_query', 'bot_response', 'timestamp')
    search_fields = ('user__username', 'user_query', 'bot_response')
    list_filter = ('timestamp', 'user')
    ordering = ('-timestamp',)

# Register your models here.
