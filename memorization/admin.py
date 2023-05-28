# https://github.com/seatgeek/thefuzz
import random
from django.contrib import admin
from .models import ImportTexts, PhraseGeneratorForTerms, WordMemorizationTest, GPTIssues, Challenge
from word.models import Terms
from thefuzz import fuzz


@admin.register(WordMemorizationTest)
class WordMemorizationTestAdmin(admin.ModelAdmin):
    list_display = ('term', 'answer', 'hit_percentage', 'id', 'created_at', 'updated_at')
    search_fields = ('id', 'term')

    def has_add_permission(self, request, obj=None):
        challenge = Challenge.objects.filter(is_active=True).last()
        if challenge:
            if WordMemorizationTest.objects.filter(challenge=challenge).count() < challenge.amount + 1:
                return True
        return False
    
    def add_view(self, request, form_url="", extra_context=None):
        challenge = Challenge.objects.filter(is_active=True).last()
        
        items = Terms.objects.filter(tags__in=list(challenge.tags.all().values_list('id', flat=True)))
        random_item = random.choice(items)

        _object = WordMemorizationTest.objects.create(**{
            "reference": str(random_item.id), 
            "term": random_item.text or None,
            "audio": random_item.pronunciation or None,
            "challenge": challenge
        })

        return self.changeform_view(request, str(_object.id), form_url, extra_context)

    def save_model(self, request, obj, form, change):
        translations = Terms.objects.filter(id=obj.reference).first().translations.all()
        percentage = 0

        for item in translations:
            ratio = fuzz.partial_ratio(str(obj.answer).lower(), str(item.term).lower())
            if ratio > percentage:
                percentage = ratio

        obj.hit_percentage = percentage
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
