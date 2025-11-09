import random
from memorization.models import Challenge, HistoryAttempt, ChallengesCompleted
from word.models import Term, Tag, ShortText
from django.shortcuts import render
from django.db.models import Count, Q
from memorization.utils import remove_tags_html


def vocabulary_test(request):
    challenge = Challenge.objects.filter(is_active=True).last()
    
    if request.method == 'POST':                     
        instance_id = request.POST.get("instance_id")
        instance = Term.objects.get(id=instance_id)            
        
        if "i_dont_know" in request.POST:
            tag = Tag.objects.get(term="study_again")
            instance.tags.add(tag)
        
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
            'message': message
        }
        return render(request, 'result_form.html', context)
    else:
        short_text = None
        short_text_obj = ShortText.objects.filter(tags__in=challenge.tags.all()).last()
        if short_text_obj:
            short_text = short_text_obj.text
        
        challenges_completed = ChallengesCompleted.objects.filter(
            challenge=challenge, completed=True
            ).values_list(
                "reference", flat=True
            )
        options = Term.objects.filter(tags__in=challenge.tags.all()).exclude(id__in=list(challenges_completed))
        
        print(f"options: {options}")
        
        if not options.count():
            context = {
                'color': 'text-green',
                'message': 'Test completed successfully.!!!!'
            }
            return render(request, 'result_form.html', context)
        
        num = random.randint(0, options.count()-1)   
        elem = options[num]
                
        options = list(elem.option_set.all().values('id', 'term').order_by('?'))
        context = {
            'short_text': short_text,
            'instance_id': elem.id,
            'sentence': elem.text,
            'options': options
        }
    return render(request, 'template_proof.html', context)
