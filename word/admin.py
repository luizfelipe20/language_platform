from django.contrib import admin

from word.models import (
    Translation,
    Word,
    Phrase
)


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    ...


@admin.register(Word)
class WordAdmin(admin.ModelAdmin):
    ...


@admin.register(Phrase)
class PhraseAdmin(admin.ModelAdmin):
    ...
