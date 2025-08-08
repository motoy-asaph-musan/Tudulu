from django.contrib import admin
from .models import InstalledEquipment, Post, Like, Comment
from django.utils.html import format_html

# @admin.register(InstalledEquipment)
# class InstalledEquipmentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'name', 'serial_number', 'location', 'date_installed', 'colored_status')
#     list_editable = ('status',)
#     list_filter = ('status', 'date_installed')
#     search_fields = ('name', 'location', 'serial_number')
#     date_hierarchy = 'date_installed'
#     list_select_related = ('added_by',)
#     raw_id_fields = ('added_by',)
    
#     def colored_status(self, obj):
#         color_map = {
#             'active': 'green',
#             'inactive': 'gray',
#             'maintenance': 'orange',
#             'retired': 'red'
#         }
#         return format_html(
#             '<span style="color: {};">{}</span>',
#             color_map.get(obj.status, 'black'),
#             obj.get_status_display()
#         )
#     colored_status.short_description = 'Status'

# equipment/admin.py
@admin.register(InstalledEquipment)
class InstalledEquipmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'serial_number', 'location', 'date_installed', 'status', 'colored_status')
    list_editable = ('status',)
    list_filter = ('status', 'date_installed')
    search_fields = ('name', 'location', 'serial_number')
    date_hierarchy = 'date_installed'
    
    def colored_status(self, obj):
        color_map = {
            'active': 'green',
            'inactive': 'gray',
            'maintenance': 'orange',
            'retired': 'red'
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            color_map.get(obj.status, 'black'),
            obj.get_status_display()
        )
    colored_status.short_description = 'Status Color'
    
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'truncated_content', 'tags', 'created_at')
    list_filter = ('created_at', 'author', 'tags')
    search_fields = ('content', 'author__username')
    raw_id_fields = ('author',)
    list_select_related = ('author',)
    
    def truncated_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    truncated_content.short_description = 'Content'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'created_at')
    list_filter = ('created_at',)
    raw_id_fields = ('user', 'post')
    list_select_related = ('user', 'post')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'post', 'truncated_content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'user__username')
    raw_id_fields = ('user', 'post')
    list_select_related = ('user', 'post')
    
    def truncated_content(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    truncated_content.short_description = 'Content'