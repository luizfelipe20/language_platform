from django.core.management.base import BaseCommand
from memorization.gpt_api import sentence_generator
from memorization.utils import remove_number_from_text
from word.models import Tags, Terms, TypePartSpeechChoices


class Command(BaseCommand):
    help = "OK"

    def handle(self, *args, **options): 
        phrasal_verbs_list = [
            "Aim At", "Ask For", "Ask Out", "Back Down", "Back Off", "Back Up", "Beat Up", "Beef Up", "Believe In", "Bite Off", "Blow Away", "Blow Off", 
            "Blow Out", "Blow Up", "Boil Down To", "Break Down", "Break In", "Break Off", "Break Out", "Break Through", "Break Up", "Bring Back", "Bring Over", 
            "Bring Up", "Brush Off", "Brush Up", "Build In", "Bump Into", "Burn Down", "Burn Out", "Burn Up", "Burst Out", "Butt In", "Call Back", "Call In",
            "Call Off", "Call Up", "Calm Down", "Care For", "Carry Away", "Carry On", "Carry Out", "Catch On", "Catch Up", "Cheat On", "Check In", "Check Out",
            "Chicken Out", "Chop Up", "Clean Out", "Clear Out", "Clear Up", "Clog Up", "Close Down", "Close Off", "Come About", "Come Across", "Come Apart",
            "Come Back", "Come Down", "Come Down To", "Come Down With", "Come In", "Come Off", "Come On", "Come Out", "Come Over", "Come Through", "Come Up",
            "Come Up With", "Con Into", "Con Out Of", "Cool Off", "Count On", "Count Up", "Cover Up", "Crack Down", "Cross Off", "Cut Back", "Cut Down", 
            "Cut Off", "Cut Out", "Cut Up", "Deal With", "Do Away With", "Do Over", "Do With", "Do Without", "Doze Off", "Dress Up", "Drop In", "Drop Off", 
            "Drop Out", "Dry Off", "Dry Out", "Dry Up", "Eat Up", "Empty Out", "End Up", "Fall Apart", "Fall Behind", "Fall Down", "Fall For", "Fall Off", 
            "Fall Out", "Fall Over", "Fall Through", "Feel Up To", "Fight Back", "Figure On", "Fill In", "Fill Out", "Fill Up", "Find Out", "Fix Up", "Flip Out",
            "Float Around", "Follow Up", "Fool Around", "Freak Out", "Get Ahead", "Get Along", "Get Around To", "Get Away", "Get Back", "Get Back At", 
            "Get Back To", "Get Behind", "Get By", "Get Down", "Get In", "Get Off", "Get Off On", "Get On", "Get Out", "Get Out Of", "Get Over", "Get Over With",
            "Get Through", "Get To", "Get Together", "Get Up", "Give Away", "Give In", "Give Out", "Give Up", "Go About", "Go After", "Go Ahead", "Go Along With", 
            "Go Around", "Go Away", "Go Back", "Go Back On", "Go Beyond", "Go By", "Go Down", "Go For", "Go In", "Go In For", "Go In", "Go Off", "Go On", 
            "Go Out", "Go Over", "Go Through With", "Go Up", "Go With", "Goof Around", "Gross Out", "Grow Out Of", "Grow Up", "Hand Back", "Hand In", "Hand Out",
            "Hand Over", "Hang Around", "Hang On", "Hang Out", "Hang Up", "Have On", "Head Back", "Head For", "Head Toward", "Hear About", "Hear Of", "Heat Up",
            "Help Out", "Hit On", "Hold Against", "Hold Off", "Hold On", "Hold Out", "Hold Up", "Hook Up", "Hurry Up", "Keep At", "Keep Away" "Keep Down", 
            "Keep From", "Keep Off", "Keep On", "Keep To", "Keep Up", "Kick Back", "Kick Out", "Knock Off", "Knock Out", "Knock Over", "Know About", "Lay Down",
            "Lay Off", "Lead Up To", "Leave Behind", "Leave Off", "Leave Out", "Leave Over", "Let Down", "Let In", "Let Off", "Let On", "Let Out", "Let Up", 
            "Lie Around", "Lift Up", "Light Up", "Lighten Up", "Line Up", "Live With", "Lock In", "Lock Out", "Lock Up", "Look Around", "Look At",  "Look Down On", 
            "Look Forward To", "Look Into", "Look Out", "Look Over", "Look Up", "Look Up", "Luck Out", "Make For", "Make Of", "Make Up", "Mess Up", "Mix Up", 
            "Monkey Around With", "Move In", "Move Out", "Narrow Down", "Pay Back", "Pay For", "Pay Off", "Pay Up", "Pick On", "Pick Out", "Pick Up", "Pile Up", 
            "Piss Off", "Plan Ahead", "Plan For", "Plan On", "Plug In", "Plug In", "Plug Up", "Point Out", "Point To", "Print Out", "Pull Off", "Pull Out",
            "Pull Over", "Pull Through", "Punch In", "Punch Out", "Put Away", "Put Back", "Put Down", "Put In", "Put Off", "Put Out", "Put Past", "Put To",
            "Put Together", "Put Up", "Put Up To", "Put Up With", "Ring Up", "Rip Off", "Rip Up", "Rule Out", "Run Across", "Run Around", "Run Down", "Run Into", 
            "Run Out", "Run Over", "Run Up", "Screw On", "Screw Out Of", "Screw Up", "See About", "Sell Out", "Set Up", "Settle Down", "Settle For", "Shake Up", 
            "Show Off", "Shut Off", "Shut Up", "Sign In", "Sign Out", "Sit Down", "Slow Down", "Sneak In", "Sneak Out", "Sort Out", "Space Out", "Stand Around", 
            "Stand For", "Stand Up", "Start Off", "Start Out", "Start Up", "Stay Off", "Stay Out", "Stay Up", "Step On", "Stick Around", "Stick Out", "Stick To",
            "Stick Up", "Stick With", "Stop Off", "Stop Over", "Straighten Out", "Stress Out", "Switch Off", "Switch On", "Take Apart", "Take Back", "Take In", 
            "Take Out", "Take Out On", "Take Up On", "Talk Down To", "Talk Into", "Talk Out Of", "Talk To", "Tear Down", "Tear Off", "Tell Apart", "Tell On",
            "Think About", "Think Ahead", "Think Up", "Throw Away", "Throw Out", "Throw Up", "Track Down", "Trade In", "Trick Into", "Try On", "Try Out", 
            "Turn Around", "Turn Down", "Turn In", "Turn Into", "Turn Off", "Turn On", "Turn Out", "Turn Over", "Turn Up", "Use Up", "Wake Up", "Wash Off", 
            "Wash Up", "Watch Out", "Wear Down", "Wear Off", "Wear Out", "Wind Up", "Wipe Off", "Wipe Out", "Wipe Up", "Work In", "Work Out", "Work Up", 
            "Wrap Up", "Zip Up"
        ]    
        count = 0
        
        for item in phrasal_verbs_list:
            request = "list of 10 sentences with the phrasal verbs SENTENCE. Be succinct and return only what was requested.".replace("SENTENCE", item)
            result = sentence_generator(request)
            gpt_senteces = str(result).splitlines()
            count += 1 

            for elem in gpt_senteces:            
                try:
                    sentence_obj, _ = Terms.objects.get_or_create(**{
                        "text": remove_number_from_text(elem),
                        "language": TypePartSpeechChoices.ENGLISH, 
                    })

                    tag_name = self.get_tag(count)
                    tag = Tags.objects.get(term=tag_name)
                    sentence_obj.tags.add(tag)

                    self.stdout.write(
                        self.style.SUCCESS(f"sentence_obj: {sentence_obj}")
                    )
                except Exception as exc:
                    print(f"exc__error: {exc}, {tag_name=}, {count=}")
                

    def get_tag(self, count):
        if count in range(0,51):
            return "phrasal_verb_01"
        elif count in range(50,101):
            return "phrasal_verb_02"
        elif count in range(100,151):
            return "phrasal_verb_03"
        elif count in range(150,201):
            return "phrasal_verb_04"
        elif count in range(200,251):
            return "phrasal_verb_05"
        elif count in range(250,301):
            return "phrasal_verb_06"
        elif count in range(300,351):
            return "phrasal_verb_07"
        elif count in range(350,401):
            return "phrasal_verb_08"
