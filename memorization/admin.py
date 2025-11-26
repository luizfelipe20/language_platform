from django.contrib import admin
from .models import (HistoryAttempt, Challenge, ChallengesCompleted)
from django.utils.html import format_html
    

@admin.register(Challenge)
class ChallengesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'get_tags', 'created_at', 'updated_at')
    search_fields = ('id', 'tags__term')
    filter_horizontal = ('tags',)
    ordering = ('-created_at',)
        
    def get_tags(self, obj):
        html = [f"<li>{item.term}</li>" for item in obj.tags.all()]
        return format_html(f"<ul>{''.join(html)}</ul>")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.username == 'admin':
            return qs.all()
        return qs.filter(user=request.user)
    
    def save_model(self, request, obj, form, change):
        if not obj.user:  
            obj.user = request.user
        super().save_model(request, obj, form, change)


@admin.register(HistoryAttempt)
class HistoryAttemptAdmin(admin.ModelAdmin):
    search_fields = ('reference__id',)
    list_display = ('id', 'reference', 'got_it_right', 'created_at', 'updated_at')


@admin.register(ChallengesCompleted)
class ChallengesCompletedAdmin(admin.ModelAdmin):
    ...