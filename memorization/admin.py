import random
from time import sleep
from django.contrib import admin
from memorization.gpt_api import sentence_generator
from memorization.similarity_validation import similarity_comparison

from memorization.utils import remove_number_from_text, standardize_text
from .models import HistoricChallenge, PhraseMaker, TranslationGeneratorForSentence, WordMemorizationRandomTest, Challenge
from word.models import Terms, Translation, TypePartSpeechChoices
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
        last_item_historic_challenge = HistoricChallenge.objects.filter(challenge__is_active=True).last()
        unavailable_sentences = []

        if last_item_historic_challenge.random:
            items = self._random_search(last_item_historic_challenge, unavailable_sentences)
            try:
                selected_item = random.choice(items)
            except IndexError as exc:
                print(f"get_form: {exc}")
                return form
        else:
            selected_item = self._ordered_search(last_item_historic_challenge)

        if not selected_item:
            return form
        
        form.base_fields['reference'].initial = selected_item.id
        form.base_fields['term'].initial = selected_item.text or None
        form.base_fields['challenge'].initial = last_item_historic_challenge.challenge
        form.base_fields['challenge'].disabled = True
        form.base_fields['historic_challenge'].initial = last_item_historic_challenge
        form.base_fields['historic_challenge'].disabled = True
        form.base_fields['hit_percentage'].disabled = True

        return form
    
    def _ordered_search(self, last_item_historic_challenge):
        sentences_already_registered = WordMemorizationRandomTest.objects.filter(
            historic_challenge=last_item_historic_challenge, hit_percentage__gte=last_item_historic_challenge.correct_percentage_considered
        ).values_list('reference', flat=True)

        item = Terms.objects.filter(
            tags__in=last_item_historic_challenge.challenge.tags.all(),                         
            language=last_item_historic_challenge.language
        ).exclude(id__in=list(sentences_already_registered)).order_by('created_at').first()
                
        return item 
    
    def _random_search(self, last_item_historic_challenge, unavailable_sentences):
        sentences_already_registered = WordMemorizationRandomTest.objects.filter(
            historic_challenge=last_item_historic_challenge, hit_percentage__gte=last_item_historic_challenge.correct_percentage_considered
        ).values('reference').annotate(total_number_of_hits=Count('reference')).order_by()
        
        for item in sentences_already_registered:
            if item.get('total_number_of_hits') >= last_item_historic_challenge.number_of_correct_answers:
                unavailable_sentences.append(item.get('reference'))

        items = Terms.objects.filter(
            tags__in=last_item_historic_challenge.challenge.tags.all(), 
            language=last_item_historic_challenge.language
        ).exclude(id__in=unavailable_sentences)    

        return items

    def save_model(self, request, obj, form, change):
        translations = Translation.objects.filter(reference=obj.reference).values_list("term", flat=True)
        percentage = 0

        for item in translations:
            _answer = standardize_text(obj.answer)
            _translation = standardize_text(item)
            similarity = similarity_comparison(_answer, _translation)

            if similarity > percentage:
                percentage = similarity

        obj.hit_percentage = percentage
        super(WordMemorizationTestAdmin, self).save_model(request, obj, form, change)
    
    def response_add(self, request, obj):
        last_item_historic_challenge = HistoricChallenge.objects.filter(challenge__is_active=True).last()

        if obj.hit_percentage >= last_item_historic_challenge.correct_percentage_considered:
            msg = f"RIGHT ANSWER!!! {obj.reference}"
            self.__increas_translations(obj)
            self.message_user(request, msg, level=messages.WARNING)
        
        number_of_times_repeated = WordMemorizationRandomTest.objects.filter(
            reference=obj.reference,
            historic_challenge=last_item_historic_challenge,
            hit_percentage__gte=last_item_historic_challenge.correct_percentage_considered
        ).count()
        
        if number_of_times_repeated >= last_item_historic_challenge.number_of_correct_answers:
            msg = f"CHALLENGE COMPLETED FOR SENTENCING: {obj.reference}"
            self.message_user(request, msg, level=messages.WARNING)
        return super(WordMemorizationTestAdmin, self).response_add(request, obj)

    def __increas_translations(self, obj):
        Translation.objects.get_or_create(**{
            "term": remove_number_from_text(obj.answer).replace('"', ''),
            "reference": Terms.objects.get(id=obj.reference),
            "language": TypePartSpeechChoices.PORTUGUESE, 
        })        

class HistoricChallengeInline(admin.TabularInline):
    model = HistoricChallenge
    extra = 0
    ordering = ('-created_at',)


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


@admin.register(PhraseMaker)
class PhraseMakerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    search_fields = ('id',)
    filter_horizontal = ('sentences', 'tags')
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['sentences']:
            super(PhraseMakerAdmin, self).save_model(request, obj, form, change)

        if not bool(obj.request):
            super(PhraseMakerAdmin, self).save_model(request, obj, form, change)

        request = str(obj.request).strip()
        result = sentence_generator(request)
        sentences = []

        for item in str(result).splitlines():
            sentence_obj, _ = Terms.objects.get_or_create(**{
                "text": remove_number_from_text(item),
                "language": TypePartSpeechChoices.ENGLISH, 
            })

            for tag in form.cleaned_data['tags']:
                sentence_obj.tags.add(tag)

            sentences.append(sentence_obj)

        form.cleaned_data['sentences'] = sentences
        obj.answer = result
        super(PhraseMakerAdmin, self).save_model(request, obj, form, change)


@admin.register(TranslationGeneratorForSentence)
class TranslationGeneratorForSentenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'sentences', 'created_at', 'updated_at')
    search_fields = ('id',)
    filter_horizontal = ('tags',)
    ordering = ('-created_at',)

    def save_model(self, request, obj, form, change):
        if form.cleaned_data['tags']:
            sentences_filtered_by_tags = Terms.objects.filter(tags__in=form.cleaned_data['tags'], language=TypePartSpeechChoices.ENGLISH)
            for sentence in sentences_filtered_by_tags:
                self.__generates_translations_for_sentences(obj, sentence)
    
        else:
            for sentence in obj.sentences.sentences.all():
                self.__generates_translations_for_sentences(obj, sentence)

        super(TranslationGeneratorForSentenceAdmin, self).save_model(request, obj, form, change)
    
    def __generates_translations_for_sentences(self, obj, sentence):
        request = str(obj.request).replace("SENTENCE", standardize_text(sentence.text)).strip()                

        print(f"__generates_translations_for_sentences: {request}")
        sleep(0.5)

        result = sentence_generator(request)

        for item in str(result).splitlines():
            try:
                Translation.objects.get_or_create(**{
                    "term": remove_number_from_text(item).replace('"', ''),
                    "reference": sentence,
                    "language": TypePartSpeechChoices.PORTUGUESE, 
                })
            except Exception as exc:
                print(f"__generates_translations_for_sentences__error: {exc}")
