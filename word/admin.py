from django.contrib import admin
from word.models import (
    Translation,
    ShortText,
    HistoryAttempt,
    Term,
    Tag
)
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilterBuilder


@admin.register(Translation)
class TranslationAdmin(admin.ModelAdmin):
    list_display = ('term', 'id', 'created_at', 'updated_at')
    search_fields = ('id', 'term', 'reference__id')
    list_filter = (
        'reference__tags',
        ("created_at", DateRangeFilterBuilder()),
    )

class TermInline(admin.TabularInline):
    model = Term
    extra = 0
    show_change_link = True
    exclude = ["tag", "obs"]


class TranslationInline(admin.TabularInline):
    model = Translation
    extra = 0


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_text', 'get_translations', 'get_tags', 'created_at', 'updated_at')
    search_fields = ('id', 'text', 'tags__term')
    filter_horizontal = ('tags', )
    inlines = [TranslationInline]
    list_filter = (
        'language',
        'tags',
        ("created_at", DateRangeFilterBuilder()),
    )
    ordering = ('-created_at',)

    def get_text(self, obj):
        return format_html(obj.text)
    
    def get_translations(self, obj):        
        html = [f"<li>{translation}</li>" for translation in Translation.objects.filter(reference=obj).values_list("term", flat=True)]
        return format_html(f"<ul>{''.join(html)}</ul>")

    def get_tags(self, obj):
        html = [f"<li>{item.term}</li>" for item in obj.tags.all()]
        return format_html(f"<ul>{''.join(html)}</ul>")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('term', 'id', 'created_at', 'updated_at')
    search_fields = ('id', 'term')
    filter_horizontal = ('tags',)


@admin.register(ShortText)
class ShortTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'completed', 'created_at', 'updated_at')


@admin.register(HistoryAttempt)
class HistoryAttemptAdmin(admin.ModelAdmin):
    search_fields = ('reference__id',)
    list_display = ('id', 'reference', 'got_it_right', 'created_at', 'updated_at')

