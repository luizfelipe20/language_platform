import random
from django.contrib import admin
from .models import ChallengeTerm, ExtractTextFromPDF, ImportTexts, PhraseGeneratorForTerms, SentencesInOrderPrecedenceTest, VerbsConjugation, WordMemorizationRandomTest, GPTIssues, Challenge
from word.models import Terms, Translation
from thefuzz import fuzz


@admin.register(WordMemorizationRandomTest)
class WordMemorizationTestAdmin(admin.ModelAdmin):
    list_display = ('term', 'answer', 'get_translations', 'lissen', 'hit_percentage', 'id', 'reference', 'created_at', 'updated_at')
    search_fields = ('id', 'term')

    def get_translations(self, obj):
        return """
                \n
                \n
        """.join([translation for translation in Translation.objects.filter(reference=obj.reference).values_list("term", flat=True)])
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(WordMemorizationTestAdmin, self).get_form(request, obj, **kwargs)        
        challenge = Challenge.objects.filter(is_active=True).last()

        if WordMemorizationRandomTest.objects.filter(challenge=challenge).count() < ChallengeTerm.objects.filter(challenge=challenge).count():
            tests_already_performed = list(WordMemorizationRandomTest.objects.filter(challenge=challenge).values_list('reference', flat=True).distinct())
            challenge_terms_ids = ChallengeTerm.objects.filter(challenge=challenge).values_list('term', flat=True).distinct()
            items = Terms.objects.filter(id__in=list(challenge_terms_ids)).exclude(id__in=tests_already_performed)
        else:
            ids = WordMemorizationRandomTest.objects.filter(challenge=challenge, hit_percentage__lte=90).values_list('reference', flat=True).distinct()
            items = Terms.objects.filter(id__in=list(ids))
        
        random_item = random.choice(items)
        form.base_fields['reference'].initial = random_item.id
        form.base_fields['term'].initial = random_item.text or None
        form.base_fields['lissen'].initial = random_item.pronunciation or None
        form.base_fields['challenge'].initial = challenge
            
        return form
    
    def save_model(self, request, obj, form, change):
        translations = Translation.objects.filter(reference=obj.reference).values_list("term", flat=True)
        percentage = 0

        for item in translations:
            ratio = fuzz.ratio(str(obj.answer).lower().replace(" ", ""), str(item).lower().replace(" ", ""))
            if ratio > percentage:
                percentage = ratio

        obj.hit_percentage = percentage
        obj.lissen = Terms.objects.get(id=obj.reference).pronunciation
        super().save_model(request, obj, form, change)


@admin.register(SentencesInOrderPrecedenceTest)
class SentencesInOrderPrecedenceTestAdmin(admin.ModelAdmin):
    list_display = ('term', 'answer', 'get_translations', 'lissen', 'hit_percentage', 'id', 'reference', 'created_at', 'updated_at')
    search_fields = ('id', 'term')

    def get_translations(self, obj):
        return "/ ---------- /".join([translation for translation in Translation.objects.filter(reference=obj.reference).values_list("term", flat=True)])
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(SentencesInOrderPrecedenceTestAdmin, self).get_form(request, obj, **kwargs)        
        challenge = Challenge.objects.filter(is_active=True).last()

        if SentencesInOrderPrecedenceTest.objects.filter(challenge=challenge).count() < ChallengeTerm.objects.filter(challenge=challenge).count():
            tests_already_performed = list(SentencesInOrderPrecedenceTest.objects.filter(challenge=challenge).values_list('reference', flat=True).distinct())
            print(f'tests_already_performed: {tests_already_performed}')

            current_term = ChallengeTerm.objects.filter(challenge=challenge).exclude(term__in=tests_already_performed).order_by('sequence_order').first().term

        else:
            ids = SentencesInOrderPrecedenceTest.objects.filter(challenge=challenge, hit_percentage__lte=90).values_list('reference', flat=True).distinct()
            items = Terms.objects.filter(id__in=list(ids))
            current_term = random.choice(items)

        form.base_fields['reference'].initial = current_term.id
        form.base_fields['term'].initial = current_term.text or None
        form.base_fields['lissen'].initial = current_term.pronunciation or None
        form.base_fields['challenge'].initial = challenge
            
        return form
    
    def save_model(self, request, obj, form, change):
        translations = Translation.objects.filter(reference=obj.reference).values_list("term", flat=True)
        percentage = 0

        for item in translations:
            ratio = fuzz.ratio(str(obj.answer).lower().replace(" ", ""), str(item).lower().replace(" ", ""))
            if ratio > percentage:
                percentage = ratio

        obj.hit_percentage = percentage
        obj.lissen = Terms.objects.get(id=obj.reference).pronunciation
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
    filter_horizontal = ('tags',)

    def get_tags(self, obj):
        return " - ".join([item.term for item in obj.tags.all()])


@admin.register(ChallengeTerm)
class ChallengeTermAdmin(admin.ModelAdmin):
    list_display = ('term', 'sequence_order', 'id', 'created_at')
    raw_id_fields = ('term', 'challenge')



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
