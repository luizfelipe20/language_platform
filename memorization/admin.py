# https://github.com/seatgeek/thefuzz
from django.contrib import admin

from memorization.gpt_api import generates_response
from .models import WritingWordMemorizationTest, AudioWordMemorizationTest, GPTIssues
from word.models import Word


@admin.register(WritingWordMemorizationTest)
class WritingWordMemorizationTestAdmin(admin.ModelAdmin):
    list_display = ('word', 'id')
    search_fields = ('id', 'word')

    def add_view(self, request, form_url="", extra_context=None):
        instance = Word.objects.last()
        _object = WritingWordMemorizationTest.objects.create(**{"word": instance, "text": instance.writing})
        return self.changeform_view(request, str(_object.id), form_url, extra_context)

@admin.register(AudioWordMemorizationTest)
class AudioWordMemorizationTestAdmin(admin.ModelAdmin):
    list_display = ('word', 'id')
    search_fields = ('id', 'word')


@admin.register(GPTIssues)
class GPTIssuesAdmin(admin.ModelAdmin):
    list_display = ('id',)
    search_fields = ('id', 'question')