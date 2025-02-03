import random
from django.contrib import admin
from .models import HistoricChallenge, MultipleChoiceMemorizationTestsOptions, UnavailableItem, WordMemorizationRandomTest, Challenge, Options
from word.models import Tag, Term, Translation
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
    

@admin.register(WordMemorizationRandomTest)
class WordMemorizationRandomTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_true', 'get_term', 'reference', 'created_at', 'updated_at')
    search_fields = ('id', 'reference')
    list_filter = ('challenge',)
    list_filter = (
        'challenge',
        ("created_at", DateRangeFilterBuilder()),
    )
    ordering = ('-created_at',)
    inlines = [OptionsInline]

    def get_term(self, obj):
        return format_html(obj.term)    
    
    def get_queryset(self, request):
        last_item_historic_challenge = HistoricChallenge.objects.filter(challenge__is_active=True).last()
        if not last_item_historic_challenge:
            return super().get_queryset(request)
        
        items = Term.objects.filter(
            tags__in=last_item_historic_challenge.challenge.tags.all(), 
            language=last_item_historic_challenge.language
        )

        if len(items) == 0:
            return super().get_queryset(request)
        
        _selected_item = random.choice(items)

        if WordMemorizationRandomTest.objects.all().count() == 0:
            obj, _ = WordMemorizationRandomTest.objects.get_or_create(**{
                "reference": _selected_item,
                "term": _selected_item.text or None,
                "challenge": last_item_historic_challenge.challenge,
                "historic_challenge": last_item_historic_challenge
            })

            _options = MultipleChoiceMemorizationTestsOptions.objects.get(reference=_selected_item)

            for option in _options.sentences_options.split(","):
                Options.objects.get_or_create(**{
                    "option": option,
                    "word_memorization_random_test": obj
                })
        return super().get_queryset(request)
     
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save_and_add_another'] = False
        return super(WordMemorizationRandomTestAdmin, self).changeform_view(request, object_id, extra_context=extra_context)
    
    def save_model(self, request, obj, form, change):
        if obj.needs_reinforcement:
            term = Term.objects.get(id=obj.reference.id)
            tag = Tag.objects.get(term="Study Again")
            term.tags.add(tag)

        last_item_historic_challenge = HistoricChallenge.objects.filter(challenge__is_active=True).last()
        unavailable_items = list(UnavailableItem.objects.values_list("reference__id", flat=True))

        available_items = Term.objects.filter(
            tags__in=last_item_historic_challenge.challenge.tags.all(), 
            language=last_item_historic_challenge.language
        ).exclude(id__in=unavailable_items)

        _count = WordMemorizationRandomTest.objects.filter(reference=obj.reference, is_true=True).count() + 1
        if (
            _count == last_item_historic_challenge.number_of_correct_answers
        ):
            UnavailableItem.objects.get_or_create(**{
                "reference": obj.reference
            })

            available_items = available_items.exclude(id=obj.reference.id)
        
        if available_items.count() == 0:
            return super().save_model(request, obj, form, change)
        
        _selected_item = random.choice(available_items)

        new_obj = WordMemorizationRandomTest.objects.create(**{
            "reference": _selected_item,
            "term": _selected_item.text,
            "challenge": last_item_historic_challenge.challenge,
            "historic_challenge": last_item_historic_challenge
        })

        _options = MultipleChoiceMemorizationTestsOptions.objects.get(reference=_selected_item)

        for option in _options.sentences_options.split(","):
            Options.objects.create(**{
                "option": option,
                "word_memorization_random_test": new_obj
            })

        super().save_model(request, obj, form, change)

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


@admin.register(MultipleChoiceMemorizationTestsOptions)
class MultipleChoiceMemorizationTestsOptionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'reference', 'created_at', 'updated_at')
    search_fields = ('id', 'reference__id', 'reference__tags__term')
    ordering = ('-created_at',)


@admin.register(Options)
class OptionAdmin(admin.ModelAdmin):
    ...


@admin.register(UnavailableItem)
class UnavailableItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'reference', 'created_at', 'updated_at')
