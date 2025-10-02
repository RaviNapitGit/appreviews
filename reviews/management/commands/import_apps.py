import csv, re
from django.core.management.base import BaseCommand
from reviews.models import App
from decimal import Decimal
from datetime import datetime

def parse_installs(s):
    if s is None:
        return 0
    s = s.strip()
    s = s.replace('+','').replace(',','')
    try:
        return int(s)
    except:
        return 0

def parse_price(p):
    try:
        return Decimal(str(p))
    except:
        return Decimal('0')

def parse_date(s):
    if not s:
        return None
    from dateutil import parser
    try:
        return parser.parse(s).date()
    except Exception:
        return None

class Command(BaseCommand):
    help = 'Import apps from CSV'
    def add_arguments(self, parser):
        parser.add_argument('csvpath')
    def handle(self, *args, **options):
        path = options['csvpath']
        count = 0
        with open(path, newline='', encoding='utf-8') as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                name = row.get('App') or row.get('name') or row.get('app')
                if not name:
                    continue
                installs = parse_installs(row.get('Installs') or row.get('installs') or '')
                price = parse_price(row.get('Price') or '0')
                rating = None
                try:
                    rating = float(row.get('Rating')) if row.get('Rating') else None
                except:
                    rating = None
                last_updated = parse_date(row.get('Last Updated') or row.get('Last_Updated') or row.get('LastUpdated'))
                app, created = App.objects.update_or_create(
                    name=name.strip(),
                    defaults={
                        'category': row.get('Category') or '',
                        'rating': rating,
                        'size': row.get('Size') or None,
                        'installs': installs,
                        'app_type': row.get('Type') or 'Free',
                        'price': price,
                        'content_rating': row.get('Content Rating') or None,
                        'genres': row.get('Genres') or None,
                        'last_updated': last_updated,
                        'current_ver': row.get('Current Ver') or None,
                        'android_ver': row.get('Android Ver') or None,
                    }
                )
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Imported/Updated {count} apps'))
