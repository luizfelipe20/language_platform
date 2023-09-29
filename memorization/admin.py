import random
from django.contrib import admin
from .models import WordMemorizationRandomTest, Challenge
from word.models import Terms, Translation
from thefuzz import fuzz
from django.utils.html import format_html
from django.db.models import Count
from rangefilter.filters import DateRangeFilterBuilder


@admin.register(WordMemorizationRandomTest)
class WordMemorizationTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_term', 'answer', 'get_translations', 'hit_percentage', 'reference', 'created_at', 'updated_at')
    search_fields = ('id', 'reference')
    list_filter = ('challenge',)
    list_filter = (
        'challenge',
        ("created_at", DateRangeFilterBuilder()),
    )

    def get_term(self, obj):
        return format_html(obj.term)
    
    def get_translations(self, obj):
        html = [f"<li>{translation}</li>" for translation in Translation.objects.filter(reference=obj.reference).values_list("term", flat=True)]
        return format_html(f"<ul>{''.join(html)}</ul>")
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(WordMemorizationTestAdmin, self).get_form(request, obj, **kwargs)        
        challenge = Challenge.objects.filter(is_active=True).last()
        unavailable_sentences = []

        sentences_already_registered = WordMemorizationRandomTest.objects.filter(
            challenge=challenge, hit_percentage__gt=challenge.correct_percentage_considered
        ).values('reference').annotate(total_number_of_hits=Count('reference')).order_by()
                
        for item in sentences_already_registered:
            if item.get('total_number_of_hits') > challenge.number_of_correct_answers:
                unavailable_sentences.append(item.get('reference'))

        items = Terms.objects.filter(tags__in=challenge.tags.all()).exclude(id__in=unavailable_sentences)
        
        if not items:
            return form
        
        random_item = random.choice(items)
        
        form.base_fields['reference'].initial = random_item.id
        form.base_fields['term'].initial = random_item.text or None
        form.base_fields['challenge'].initial = challenge
        form.base_fields['challenge'].disabled = True
        form.base_fields['hit_percentage'].disabled = True

        return form
    
    def save_model(self, request, obj, form, change):
        translations = Translation.objects.filter(reference=obj.reference).values_list("term", flat=True)
        percentage = 0

        for item in translations:
            ratio = fuzz.partial_ratio(str(obj.answer).lower().replace(" ", ""), str(item).lower().replace(" ", ""))
            if ratio > percentage:
                percentage = ratio

        obj.hit_percentage = percentage
        super().save_model(request, obj, form, change)


@admin.register(Challenge)
class ChallengesAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'number_of_correct_answers', 'get_tags', 'created_at', 'updated_at')
    search_fields = ('id', 'tags__term')
    filter_horizontal = ('tags',)

    def get_tags(self, obj):
        return " - ".join([item.term for item in obj.tags.all()])