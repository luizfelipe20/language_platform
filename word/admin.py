from django.contrib import admin

from word.models import (
    Translation,
    Terms,
    Tags
)


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('term', 'id')
    search_fields = ('id', 'term')


@admin.register(Terms)
class WordAdmin(admin.ModelAdmin):
    list_display = ('text', 'pronunciation', 'id')
    search_fields = ('id', 'text')
    filter_horizontal = ('translations', 'tags')


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('term', 'id')
    search_fields = ('id', 'term')
