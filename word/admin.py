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
    list_display = ('text', 'get_translations', 'get_tags', 'created_at', 'updated_at', 'pronunciation', 'id')
    search_fields = ('id', 'text', 'tags__term')
    filter_horizontal = ('translations', 'tags')
    list_filter = ["tags"]

    def get_translations(self, obj):
        return "\n".join([item.term for item in obj.translations.all()])

    def get_tags(self, obj):
        return " - ".join([item.term for item in obj.tags.all()])


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('term', 'id', 'created_at', 'updated_at')
    search_fields = ('id', 'term')

