from django.contrib import admin
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import CheckboxFilter

from products.widgets import CustomUnfoldAdminImageFieldWidget


from products.models import *


@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ('title', 'is_pinned', 'order', 'published_at')
    list_display_links = ('title', 'is_pinned', 'order', 'published_at')
    search_fields = ('title', 'link')
    list_filter = ('is_pinned', 'show_for_youtube', 'show_for_tiktok', 'show_for_instagram', 'created_at', 'updated_at')
    list_filter_submit = True
    compressed_fields = True
    warn_unsaved_form = True
    list_fullwidth = True
    ordering = ('-is_pinned', 'order', '-published_at')

    fieldsets = (
        (None, {'fields': ('title', 'link', 'is_pinned', 'order')}),
        ("Social Media", {'fields': ('show_for_youtube', 'show_for_tiktok', 'show_for_instagram')}),
        ("File", {'fields': ('file',)}),
        ('Timestamps', {'fields': ('published_at', 'created_at', 'updated_at'), 'classes': ('collapse',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('title', 'link', 'is_pinned', 'order')}),
        ("Social Media", {'fields': ('show_for_youtube', 'show_for_tiktok', 'show_for_instagram')}),
        ("File", {'fields': ('file',)}),
        ('Timestamps', {'fields': ('published_at',)}),

    )
    readonly_fields = ('id', 'created_at', 'updated_at')


    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['file'].widget = CustomUnfoldAdminImageFieldWidget()
        return form