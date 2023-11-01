import random
from django.contrib import admin

from memorization.utils import standardize_text
from .models import WordMemorizationRandomTest, Challenge
from word.models import Terms, Translation
from thefuzz import fuzz
from django.utils.html import format_html
from django.db.models import Count
from rangefilter.filters import DateRangeFilterBuilder
from django.contrib import messages


@admin.register(WordMemorizationRandomTest)
class WordMemorizationTestAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'get_translations', 'get_term', 'hit_percentage', 'reference', 'created_at', 'updated_at')
    search_fields = ('id', 'reference')
    list_filter = ('challenge',)
    list_filter = (
        'challenge',
        ("created_at", DateRangeFilterBuilder()),
    )
    ordering = ('-created_at',)

    def get_term(self, obj):
        return format_html(obj.term)
    
    def get_translations(self, obj):
        html = [f"<li>{translation}</li>" for translation in Translation.objects.filter(reference=obj.reference).values_list("term", flat=True)]
        return format_html(f"<ul>{''.join(html)}</ul>")
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(WordMemorizationTestAdmin, self).get_form(request, obj, **kwargs)        
        challenge = Challenge.objects.filter(is_active=True).last()
        unavailable_sentences = []

        if challenge.random:
            items = self._random_search(challenge, unavailable_sentences)
            selected_item = random.choice(items)
        else:
            selected_item = self._ordered_search(challenge)

        if not items:
            return form
        
        form.base_fields['reference'].initial = selected_item.id
        form.base_fields['term'].initial = selected_item.text or None
        form.base_fields['challenge'].initial = challenge
        form.base_fields['challenge'].disabled = True
        form.base_fields['hit_percentage'].disabled = True

        return form
    
    def _ordered_search(self, challenge):
        sentences_already_registered = WordMemorizationRandomTest.objects.filter(
            challenge=challenge, hit_percentage__gt=challenge.correct_percentage_considered
        ).values('reference').order_by()
                
        return Terms.objects.filter(tags__in=challenge.tags.all(), language=challenge.language).exclude(id__in=sentences_already_registered).first()  
    
    def _random_search(self, challenge, unavailable_sentences):
        sentences_already_registered = WordMemorizationRandomTest.objects.filter(
            challenge=challenge, hit_percentage__gt=challenge.correct_percentage_considered
        ).values('reference').annotate(total_number_of_hits=Count('reference')).order_by()
                
        for item in sentences_already_registered:
            if item.get('total_number_of_hits') >= challenge.number_of_correct_answers:
                unavailable_sentences.append(item.get('reference'))

        items = Terms.objects.filter(tags__in=challenge.tags.all(), language=challenge.language).exclude(id__in=unavailable_sentences)    

        return items

    def save_model(self, request, obj, form, change):
        translations = Translation.objects.filter(reference=obj.reference).values_list("term", flat=True)
        percentage = 0

        for item in translations:
            _answer = standardize_text(obj.answer)
            _translation = standardize_text(item)
            ratio = fuzz.partial_ratio(_answer, _translation)
            if ratio > percentage:
                percentage = ratio

        obj.hit_percentage = percentage
        super(WordMemorizationTestAdmin, self).save_model(request, obj, form, change)
    
    def response_add(self, request, obj):
        challenge = Challenge.objects.filter(is_active=True).last()

        if obj.hit_percentage > 85:
            msg = f"RIGHT ANSWER!!! {obj.reference}"
            self.message_user(request, msg, level=messages.WARNING)
        if WordMemorizationRandomTest.objects.filter(reference=obj.reference, hit_percentage__gte=85).count() >= challenge.number_of_correct_answers:
            msg = f"CHALLENGE COMPLETED FOR SENTENCING: {obj.reference}"
            self.message_user(request, msg, level=messages.WARNING)
        return super(WordMemorizationTestAdmin, self).response_add(request, obj)

@admin.register(Challenge)
class ChallengesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'language', 'random', 'is_active', 'number_of_correct_answers', 'get_tags', 'created_at', 'updated_at')
    search_fields = ('id', 'tags__term')
    filter_horizontal = ('tags',)
    ordering = ('-created_at',)
    
    def get_tags(self, obj):
        return " - ".join([item.term for item in obj.tags.all()])