from django.contrib import admin

from word.models import (
    Translation,
    Word,
    Phrase,
    Tags
)


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('term', 'id')
    search_fields = ('id', 'term')


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    list_display = ('writing', 'id')
    search_fields = ('id', 'writing')
    filter_horizontal = ('translations',)


@admin.register(Phrase)
class PhraseAdmin(admin.ModelAdmin):
    list_display = ('terms', 'id')
    search_fields = ('id', 'term')


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('term', 'id')
    search_fields = ('id', 'term')
