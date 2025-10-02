import csv
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from reviews.models import App, Review

User = get_user_model()


def clean_val(v):
    if v is None:
        return ''
    s = str(v).strip()
    if s.lower() in ('nan', 'none', ''):
        return ''
    return s


class Command(BaseCommand):
    help = 'Import reviews CSV'

    def add_arguments(self, parser):
        parser.add_argument('csvpath')

    def handle(self, *args, **options):
        path = options['csvpath']
        importer, _ = User.objects.get_or_create(username='importer', defaults={'is_active': True})
        count = 0
        with open(path, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                app_name = clean_val(row.get('App') or row.get('app') or row.get('App Name'))
                text = clean_val(row.get('Translated_Review') or row.get('Review') or row.get('translated_review'))
                if not text:
                    continue
                try:
                    app = App.objects.get(name=app_name)
                except App.DoesNotExist:
                    self.stdout.write(self.style.WARNING(f'Skipping review for unknown app: {app_name}'))
                    continue
                sentiment = clean_val(row.get('Sentiment')) or None
                polarity = clean_val(row.get('Sentiment_Polarity')) or None
                subjectivity = clean_val(row.get('Sentiment_Subjectivity')) or None
                r = Review.objects.create(
                    app=app,
                    author=importer,
                    supervisor=None,
                    text=text,
                    sentiment=sentiment,
                    sentiment_polarity=float(polarity) if polarity else None,
                    sentiment_subjectivity=float(subjectivity) if subjectivity else None,
                    status='APPROVED'
                )
                app.reviews_count = app.reviews.filter(status='APPROVED').count()
                app.save()
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Imported {count} reviews'))
