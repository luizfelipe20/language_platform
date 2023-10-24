from django.core.management.base import BaseCommand
from memorization.models import Challenge, WordMemorizationRandomTest
from django.db.models import Count


class Command(BaseCommand):
    help = "OK"

    def add_arguments(self, parser):
        parser.add_argument("--challenge", nargs="+", type=str)

    def handle(self, *args, **options): 
        sentences_to_review = []

        for challenge_name in options.get("challenge"):
            challenge_obj = Challenge.objects.filter(name=challenge_name).last()

            if not challenge_obj:
                raise Exception("Challenge not registered in the database!!!")

        sentences_with_index_below_average = WordMemorizationRandomTest.objects.filter(
            challenge=challenge_obj, hit_percentage__lt=85
        ).values('reference').annotate(total_number_of_hits=Count('reference')).order_by()

        for item in sentences_with_index_below_average:
            if item.get('total_number_of_hits') > 2:
                sentences_to_review.append(item.get('reference'))

        if not sentences_to_review:
            self.stdout.write(
                self.style.WARNING('No changes were made !!!')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'Successfully !!! {sentences_to_review}')
            )