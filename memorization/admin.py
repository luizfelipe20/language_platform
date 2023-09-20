import random
from django.contrib import admin
from .models import WordMemorizationRandomTest, Challenge
from word.models import Terms, Translation
from thefuzz import fuzz
from django.utils.html import format_html


@admin.register(WordMemorizationRandomTest)
class WordMemorizationTestAdmin(admin.ModelAdmin):
    list_display = ('term', 'answer', 'get_translations', 'hit_percentage', 'id', 'reference', 'created_at', 'updated_at')
    search_fields = ('id', 'term')

    def get_translations(self, obj):
        html = [f"<li>{translation}</li>" for translation in Translation.objects.filter(reference=obj.reference).values_list("term", flat=True)]
        return format_html(f"<ul>{''.join(html)}</ul>")
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(WordMemorizationTestAdmin, self).get_form(request, obj, **kwargs)        
        challenge = Challenge.objects.filter(is_active=True).last()
        unavailable_sentences = []

        sentences_already_registered = WordMemorizationRandomTest.objects.filter(challenge=challenge, hit_percentage__lte=85).values_list('reference', flat=True).distinct()
        
        for item in sentences_already_registered:
            if WordMemorizationRandomTest.objects.filter(reference=item).count() > 9:
                unavailable_sentences.append(item)

        items = Terms.objects.exclude(id__in=unavailable_sentences)
        
        random_item = random.choice(items)
        form.base_fields['reference'].initial = random_item.id
        form.base_fields['term'].initial = random_item.text or None
        form.base_fields['challenge'].initial = challenge
            
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
    list_display = ('id', 'is_active', 'amount', 'get_tags', 'created_at', 'updated_at')
    search_fields = ('id', 'tags__term')
    filter_horizontal = ('tags',)

    def get_tags(self, obj):
        return " - ".join([item.term for item in obj.tags.all()])