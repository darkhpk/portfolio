from django.contrib import admin
from .models import CodeSession

@admin.register(CodeSession)
class CodeSessionAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'language', 'created_at', 'updated_at']
    search_fields = ['session_id']
    readonly_fields = ['created_at', 'updated_at']
