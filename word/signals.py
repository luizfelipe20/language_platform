from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta
from word.models import TotalStudyTimeLog


@receiver(user_logged_in)
def save_entry_time(sender, request, user, **kwargs):
    TotalStudyTimeLog.objects.create(**{
        'login_time': timezone.now() - timedelta(hours=3),
        'session_id': request.session.session_key,
        'status':  'on',
        'user': request.user
    })

@receiver(user_logged_out)
def save_departure_time(sender, request, user, **kwargs):
    if TotalStudyTimeLog.objects.exists():
        TotalStudyTimeLog.objects.create(**{
            'login_time': timezone.now() - timedelta(hours=3),
            'session_id': request.session.session_key,
            'status':  'off',
            'user': request.user
        })

