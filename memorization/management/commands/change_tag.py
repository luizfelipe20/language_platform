from django.core.management.base import BaseCommand
from word.models import Tags, Terms


class Command(BaseCommand):
    help = "OK"

    def add_arguments(self, parser):
        parser.add_argument("--interval", nargs="+", type=str)

        parser.add_argument("--tag", nargs="+", type=str)

    def handle(self, *args, **options): 
        terms = []

        if options.get("tag"):
            name_tag_1, name_tag_2 = options.get("tag")[0].split(",")
            tag_1 = Tags.objects.filter(term=name_tag_1).last()
            tag_2 = Tags.objects.filter(term=name_tag_2).last()

            terms = Terms.objects.filter(tags__in=[tag_1]).order_by('created_at')

        if options.get("interval"):
            interval_1, interval_2 = options.get("interval")[0].split(",")
        
            terms = terms[int(interval_1):int(interval_2)]

        for elem in terms:
            elem.tags.remove(tag_1)
            elem.tags.add(tag_2)

        if not terms:
            self.stdout.write(
                self.style.WARNING('No changes were made !!!')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('Successfully !!!')
            )