from django.contrib import admin
from .models import WritingWordMemorizationTest, AudioWordMemorizationTest
from word.models import Word


@admin.register(WritingWordMemorizationTest)
class WritingWordMemorizationTestAdmin(admin.ModelAdmin):
    list_display = ('word', 'id')
    search_fields = ('id', 'word')

    def add_view(self, request, form_url="", extra_context=None):
        instance = Word.objects.last()
        _object = WritingWordMemorizationTest.objects.create(**{"word": instance, "text": instance.writing})
        # input("******************")
        return self.changeform_view(request, str(_object.id), form_url, extra_context)

@admin.register(AudioWordMemorizationTest)
class AudioWordMemorizationTestAdmin(admin.ModelAdmin):
    list_display = ('word', 'id')
    search_fields = ('id', 'word')