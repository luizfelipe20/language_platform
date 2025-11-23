import os
import random
from memorization.models import Challenge, HistoryAttempt, ChallengesCompleted
from word.models import Term, ShortText
from django.shortcuts import render


servidor = os.environ.get("SERVIDOR")


def vocabulary_test(request):
    challenge = Challenge.objects.filter(is_active=True).last()
    
    if request.method == 'POST':                     
        instance_id = request.POST.get("instance_id")
        instance = Term.objects.get(id=instance_id)            
                
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
            if challenge.writing:
                short_text = short_text_obj.text
            if challenge.hearing:
                short_text_audio = short_text_obj.audio.url
            if challenge.translation:
                short_text_translation = short_text_obj.translation
            if challenge.phonetic_transcription:
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
        context = {
            'short_text': short_text,
            'short_text_audio': short_text_audio,
            'short_text_translation': short_text_translation,
            'short_text_phonetic_transcription': short_text_phonetic_transcription,
            'instance_id': elem.id,
            'sentence': elem.text,
            'options': options
        }
    return render(request, 'template_proof.html', context)
