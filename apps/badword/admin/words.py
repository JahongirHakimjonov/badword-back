from django.contrib import admin
from unfold.admin import ModelAdmin

from apps.badword.models import Word


@admin.register(Word)
class WordAdmin(ModelAdmin):
    list_display = ["word", "is_active"]
    search_fields = ["word"]
    list_filter = ["is_active"]
    actions = ["activate", "deactivate"]
    list_editable = ["is_active"]

    def activate(self, request, queryset):
        queryset.update(is_active=True)

    activate.short_description = "Activate selected words"

    def deactivate(self, request, queryset):
        queryset.update(is_active=False)

    deactivate.short_description = "Deactivate selected words"
