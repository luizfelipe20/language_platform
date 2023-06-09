# https://github.com/seatgeek/thefuzz
import random
from django.contrib import admin
from .models import ExtractTextFromPDF, ImportTexts, PhraseGeneratorForTerms, WordMemorizationTest, GPTIssues, Challenge
from word.models import Terms
from thefuzz import fuzz


@admin.register(WordMemorizationTest)
class WordMemorizationTestAdmin(admin.ModelAdmin):
    list_display = ('term', 'answer', 'get_translations', 'audio', 'hit_percentage', 'id', 'reference', 'created_at', 'updated_at')
    search_fields = ('id', 'term')

    def get_translations(self, obj):
        return "\n".join([translation.term for translation in Terms.objects.filter(id=obj.reference).first().translations.all()])
        
    def has_add_permission(self, request, obj=None):
        challenge = Challenge.objects.filter(is_active=True).last()
        if challenge:
            if WordMemorizationTest.objects.filter(challenge=challenge).count() < challenge.amount + 1:
                return True
        return False
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(WordMemorizationTestAdmin, self).get_form(request, obj, **kwargs)        
        challenge = Challenge.objects.filter(is_active=True).last()
        items = Terms.objects.filter(tags__in=list(challenge.tags.all().values_list('id', flat=True)))
        random_item = random.choice(items)
        
        form.base_fields['reference'].initial = random_item.id

        form.base_fields['term'].initial = random_item.text or None

        form.base_fields['audio'].initial = random_item.pronunciation or None

        form.base_fields['challenge'].initial = challenge

        return form
    
    def save_model(self, request, obj, form, change):
        translations = Terms.objects.get(id=obj.reference).translations.all()
        percentage = 0

        for item in translations:
            ratio = fuzz.partial_ratio(str(obj.answer).lower(), str(item.term).lower())
            if ratio > percentage:
                percentage = ratio

        obj.hit_percentage = percentage
        obj.audio = Terms.objects.get(id=obj.reference).pronunciation
        super().save_model(request, obj, form, change)


@admin.register(GPTIssues)
class GPTIssuesAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at', 'issue')
    search_fields = ('id', 'issue')
    filter_horizontal = ('tags', )


@admin.register(Challenge)
class ChallengesAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_active', 'created_at', 'updated_at')
    search_fields = ('id', 'tags__term')
    filter_horizontal = ('tags', )


@admin.register(ImportTexts)
class ImportTextsAdmin(admin.ModelAdmin):
    list_display = ('id', )
    search_fields = ('id', 'term')
    filter_horizontal = ('tags', )


@admin.register(PhraseGeneratorForTerms)
class PhraseGeneratorForTermsAdmin(admin.ModelAdmin):
    list_display = ('id', )
    search_fields = ('id', 'terms')
    filter_horizontal = ('tags', )


@admin.register(ExtractTextFromPDF)
class ExtractTextFromPDFAdmin(admin.ModelAdmin):
    search_fields = ('id', 'link')