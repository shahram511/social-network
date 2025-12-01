from django.contrib import admin

from frienship.models import Friendship

# Register your models here.

@admin.register(Friendship)
class FriendshipAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['sender__username', 'receiver__username']
    list_editable = ['status']
    readonly_fields = ['created_at', 'updated_at']
    
    # def has_change_permission(self, request, obj=None):
    #     return False
    
    # def has_delete_permission(self, request, obj=None):
    #     return False
    
    # def has_add_permission(self, request, obj=None):
    #     return False
    
    # def get_readonly_fields(self, request, obj=None):
    #     return ['sender', 'receiver', 'status', 'created_at', 'updated_at']