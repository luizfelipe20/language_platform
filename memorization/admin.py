import random
from django.contrib import admin
from .models import ExtractTextFromPDF, ImportTexts, PhraseGeneratorForTerms, VerbsConjugation, WordMemorizationTest, GPTIssues, Challenge
from word.models import Terms, Translation
from thefuzz import fuzz


@admin.register(WordMemorizationTest)
class WordMemorizationTestAdmin(admin.ModelAdmin):
    list_display = ('term', 'answer', 'get_translations', 'audio', 'hit_percentage', 'id', 'reference', 'created_at', 'updated_at')
    search_fields = ('id', 'term')

    def get_translations(self, obj):
        return ", \n".join([translation for translation in Translation.objects.filter(reference=obj.reference).values_list("term", flat=True)])
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(WordMemorizationTestAdmin, self).get_form(request, obj, **kwargs)        
        challenge = Challenge.objects.filter(is_active=True).last()

        if WordMemorizationTest.objects.filter(challenge=challenge).count() < challenge.amount:
            items = Terms.objects.filter(
                tags__in=list(challenge.tags.all().values_list('id', flat=True))
                ).exclude(
                id__in=list(WordMemorizationTest.objects.filter(challenge=challenge).values_list('reference', flat=True))
            )

            if challenge.phrases_associated_with_term:
                items = Terms.objects.filter(reference__in=items)
            
        else:
            ids = WordMemorizationTest.objects.filter(challenge=challenge, hit_percentage__gte=90, hit_percentage__lte=100).values_list('reference', flat=True).distinct()
            reference_ids = WordMemorizationTest.objects.values_list('reference', flat=True).exclude(reference__in=ids)
            items = Terms.objects.filter(id__in=list(reference_ids))
        
        if items:
            random_item = random.choice(items)
            form.base_fields['reference'].initial = random_item.id
            form.base_fields['term'].initial = random_item.text or None
            form.base_fields['audio'].initial = random_item.pronunciation or None
            form.base_fields['challenge'].initial = challenge
            
        return form
    
    def save_model(self, request, obj, form, change):
        translations = Translation.objects.filter(reference=obj.reference).values_list("term", flat=True)
        percentage = 0

        for item in translations:
            ratio = fuzz.partial_ratio(str(obj.answer).lower(), str(item).lower())
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
    list_display = ('id', 'is_active', 'amount', 'get_tags', 'created_at', 'updated_at')
    search_fields = ('id', 'tags__term')
    filter_horizontal = ('tags', )

    def get_tags(self, obj):
        return " - ".join([item.term for item in obj.tags.all()])


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


@admin.register(VerbsConjugation)
class VerbsConjugationAdmin(admin.ModelAdmin):
    search_fields = ('id', 'verbs')
    list_display = ('id', 'verbs')
    filter_horizontal = ('tags', )
