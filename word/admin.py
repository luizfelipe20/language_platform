import re
import json
from django.contrib import admin
from memorization.gpt_api import sentence_generator
from word.models import (
    Option,
    ShortText,
    TotalStudyTimeLog,
    Term,
    Tag,
    TypePartSpeechChoices,
    format_names_for_tags
)
from django.utils.html import format_html
from rangefilter.filters import DateRangeFilterBuilder


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('term', 'id', 'created_at', 'updated_at')
    search_fields = ('id', 'term', 'reference__id')
    list_filter = (
        'reference__tags',
        ("created_at", DateRangeFilterBuilder()),
    )

class TermInline(admin.TabularInline):
    model = Term
    extra = 0
    show_change_link = True
    exclude = ["tag", "obs"]


class OptionInline(admin.TabularInline):
    model = Option
    extra = 0


@admin.register(Term)
class TermAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_text', 'get_options', 'get_tags', 'created_at', 'updated_at')
    search_fields = ('id', 'text', 'tags__term')
    filter_horizontal = ('tags', )
    inlines = [OptionInline]
    list_filter = (
        'language',
        'tags',
        ("created_at", DateRangeFilterBuilder()),
    )
    ordering = ('-created_at',)

    def get_text(self, obj):
        return format_html(obj.text)
    
    def get_options(self, obj):        
        html = [f"<li>{option}</li>" for option in Option.objects.filter(reference=obj).values_list("term", flat=True)]
        return format_html(f"<ul>{''.join(html)}</ul>")

    def get_tags(self, obj):
        html = [f"<li>{item.term}</li>" for item in obj.tags.all()]
        return format_html(f"<ul>{''.join(html)}</ul>")


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('term', 'id', 'created_at', 'updated_at')
    search_fields = ('id', 'term')
    filter_horizontal = ('tags',)


@admin.register(ShortText)
class ShortTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    filter_horizontal = ('tags', )
    
    def transcription_into_portuguese(self, obj):
        _request_gpt = f"""
        {obj.text}
        Break the above text into sentences in the following format
        <p><b>phrase in English</b><br>
        <i>Write how the phrase would be pronounced in Portuguese.</i></p>
        """
        ShortText.objects.filter(id=obj.id).update(phonetic_transcription_portuguese=sentence_generator(_request_gpt))
    
    def question_generator(self, obj, tag_obj):
        _request_gpt = f"""
        {obj.text}
        {obj.instruction_ia}
        """        
        _result_gpt = sentence_generator(_request_gpt)
        json_str = re.search(r'\{.*\}', _result_gpt, re.DOTALL).group()
        elems = json.loads(json_str)['questions']
        for obj_chat_gpt in elems:
            sentence_obj, _ = Term.objects.get_or_create(**{
                "text": obj_chat_gpt['question'],
                "reference": ShortText.objects.get(id=obj.id),
                "language": TypePartSpeechChoices.ENGLISH, 
            })
            sentence_obj.tags.set([tag_obj])
            
            for option in obj_chat_gpt['options']:
                Option.objects.get_or_create(**{
                    "term": option,
                    "right_option": option in obj_chat_gpt['correct_answer'],
                    "reference": sentence_obj,
                    "language": TypePartSpeechChoices.PORTUGUESE, 
                })
                
    def get_form(self, request, obj=None, **kwargs):
        if obj: 
            short_text = ShortText.objects.get(id=obj.id)
            tag_name = format_names_for_tags(obj.title)
            tag_obj = Tag.objects.get(term=tag_name)
            
            if len(obj.tags.all()) == 0:
                short_text.tags.set([tag_obj])
            
            if not obj.phonetic_transcription_portuguese:
                self.transcription_into_portuguese(obj)
            
            if Term.objects.filter(reference__id=obj.id).count() < 12:
                self.question_generator(obj, tag_obj)
                
        form = super().get_form(request, obj, **kwargs)
        if obj is None:
            form.base_fields['instruction_ia'].initial = """
            Acting as an English teacher assessing a student's comprehension of the text above, generate twelve multiple-choice 
            questions where only one option is correct, and return the result in JSON format. The JSON file must contain the keys: 
            "question", "options", "correct_answer".
            """    
        return form
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.username == 'admin':
            return qs.all()
        return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        if not obj.user:  
            obj.user = request.user
        super().save_model(request, obj, form, change)

    
@admin.register(TotalStudyTimeLog)
class TotalStudyTimeLogAdmin(admin.ModelAdmin):
    list_display = ('login_time', 'session_id', 'status')
    ordering = ('-login_time',)

