from django.contrib import admin
from .models import (HistoricChallenge, Challenge, Options)
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilterBuilder
from django.forms import Textarea
from django.db import models


class OptionsInline(admin.TabularInline):
    model = Options
    extra = 0
    ordering = ('created_at',)
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows':1, 'cols':120})},
    }
    

class HistoricChallengeInline(admin.TabularInline):
    model = HistoricChallenge
    extra = 0
    ordering = ('created_at',)
    

@admin.register(Challenge)
class ChallengesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'get_tags', 'created_at', 'updated_at')
    search_fields = ('id', 'tags__term')
    filter_horizontal = ('tags',)
    ordering = ('-created_at',)
    inlines = [HistoricChallengeInline]
        
    def get_tags(self, obj):
        html = [f"<li>{item.term}</li>" for item in obj.tags.all()]
        return format_html(f"<ul>{''.join(html)}</ul>")


@admin.register(Options)
class OptionAdmin(admin.ModelAdmin):
    ...
