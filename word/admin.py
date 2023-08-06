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


class TermsInline(admin.TabularInline):
    model = Terms
    extra = 0
    show_change_link = True
    exclude = ["tags", "obs"]


class TranslationInline(admin.TabularInline):
    model = Translation
    extra = 0


@admin.register(Terms)
class TermsAdmin(admin.ModelAdmin):
    list_display = ('text', 'get_translations', 'get_tags', 'created_at', 'updated_at', 'pronunciation', 'id')
    search_fields = ('id', 'text', 'tags__term')
    filter_horizontal = ('tags', )
    inlines = [TermsInline, TranslationInline]

    def get_translations(self, obj):
        return "/ ---------- /".join([item.term for item in Translation.objects.filter(reference=obj)])

    def get_tags(self, obj):
        return "/ ---------- /".join([item.term for item in obj.tags.all()])


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('term', 'id', 'created_at', 'updated_at')
    search_fields = ('id', 'term')
    filter_horizontal = ('tags',)

