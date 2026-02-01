import re
import os
import random
from django.utils import timezone
from django.db.models import Count
from datetime import timedelta
from memorization.models import Challenge, HistoryAttempt, ChallengesCompleted
from word.models import Term, ShortText, TotalStudyTimeLog
from django.shortcuts import render


servidor = os.environ.get("SERVIDOR")


def logged_in_time_period(request):
    lits_times = []
    now = timezone.now() - timedelta(hours=3)
    for item in TotalStudyTimeLog.objects.filter(login_time__date=now).distinct('session_id'):
        instance_time_entry = TotalStudyTimeLog.objects.filter(
            session_id=item.session_id, user=request.user, status='on').last()
        instance_time_departure = TotalStudyTimeLog.objects.filter(
            session_id=item.session_id, user=request.user, status='off').last()
        if instance_time_departure and instance_time_entry:
            time_diff = instance_time_departure.login_time - instance_time_entry.login_time
            lits_times.append(time_diff.seconds)

    last_time_entry = TotalStudyTimeLog.objects.filter(
        session_id=request.session.session_key, 
        status='on'
    ).last().login_time
    logged_time = (now - last_time_entry).seconds
    _total_time_minutes = (sum(lits_times) + logged_time) // 60
    return _total_time_minutes

def remover_pre(texto):
    return re.sub(r'</?pre[^>]*>', '', texto, flags=re.IGNORECASE)

def vocabulary_test(request):
    challenge = Challenge.objects.filter(user=request.user, is_active=True).last()
    
    if request.method == 'POST':                     
        sentence_id = request.POST.get("sentence_id")
        instance = Term.objects.get(id=sentence_id)            
                
        answer_option_form = request.POST.get('answer_option')
        answer_option = instance.option_set.filter(right_option=True).last()
        got_it_right = str(answer_option.id) == answer_option_form
            
        HistoryAttempt.objects.create(**{
            "reference": instance,
            "got_it_right": got_it_right,
            "challenge": challenge
        })
        
        if HistoryAttempt.objects.filter(reference=instance, challenge=challenge, got_it_right=True).count() == challenge.number_of_correct_answers:
            ChallengesCompleted.objects.create(**{
                "reference": instance,
                "completed": True,
                "challenge": challenge
            })

        message = 'Wrong answer!!!'
        color = 'text-red'
        if got_it_right:
            message = 'Correct answer!!!'
            color = 'text-green'

        context = {
            'color': color,
            'message': message,
            'servidor': servidor
        }
        return render(request, 'result_form.html', context)
    else:
        short_text = None
        short_text_audio = None
        short_text_translation = None
        short_text_phonetic_transcription = None

        short_text_obj = ShortText.objects.filter(tags__in=challenge.tags.all()).last()
        if short_text_obj:            
            short_text = short_text_obj.text
            short_text_audio = short_text_obj.audio.url
            short_text_translation = short_text_obj.translation
            short_text_phonetic_transcription = short_text_obj.phonetic_transcription_portuguese
     
        challenges_completed = ChallengesCompleted.objects.filter(
            challenge=challenge, completed=True
            ).values_list(
                "reference", 
                flat=True
            )
        options = Term.objects.filter(tags__in=challenge.tags.all()).exclude(id__in=list(challenges_completed))
        
        if not options.count():
            context = {
                'color': 'text-green',
                'message': 'Test completed successfully.!!!!',
                'servidor': servidor
            }
            return render(request, 'result_form.html', context)
        
        num = random.randint(0, options.count()-1)   
        elem = options[num]
                
        options = list(elem.option_set.all().values('id', 'term').order_by('?'))
        total_time_minutes = logged_in_time_period(request)

        number_correct_answers = HistoryAttempt.objects.filter(
            got_it_right=True,
            challenge=challenge
        ).values('reference', 'challenge').annotate(total=Count('id')).filter(
            total=challenge.number_of_correct_answers
        ).count()
        
        context = {
            'short_text': short_text,
            'number_correct_answers': number_correct_answers,
            'short_text_audio': short_text_audio,
            'short_text_translation': short_text_translation,
            'short_text_phonetic_transcription': short_text_phonetic_transcription,
            'sentence_id': elem.id,
            'sentence': elem.text,
            'options': options,
            'minutes': total_time_minutes,
            'servidor': servidor
        }
    return render(request, 'template_proof.html', context)
