from django.db import migrations, models
import django.db.models.deletion
from django.conf import settings

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='App',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(db_index=True, max_length=255, unique=True)),
                ('category', models.CharField(max_length=128)),
                ('rating', models.FloatField(null=True)),
                ('reviews_count', models.IntegerField(default=0)),
                ('size', models.CharField(blank=True, max_length=64, null=True)),
                ('installs', models.IntegerField(db_index=True, default=0)),
                ('app_type', models.CharField(choices=[('Free','Free'),('Paid','Paid')], default='Free', max_length=8)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=6)),
                ('content_rating', models.CharField(blank=True, max_length=64, null=True)),
                ('genres', models.CharField(blank=True, max_length=255, null=True)),
                ('last_updated', models.DateField(blank=True, null=True)),
                ('current_ver', models.CharField(blank=True, max_length=64, null=True)),
                ('android_ver', models.CharField(blank=True, max_length=64, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KeyValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=128, unique=True)),
                ('value', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('sentiment', models.CharField(choices=[('Positive','Positive'),('Neutral','Neutral'),('Negative','Negative')], blank=True, max_length=8, null=True)),
                ('sentiment_polarity', models.FloatField(blank=True, null=True)),
                ('sentiment_subjectivity', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(choices=[('PENDING','PENDING'),('APPROVED','APPROVED'),('REJECTED','REJECTED')], db_index=True, default='PENDING', max_length=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved_at', models.DateTimeField(blank=True, null=True)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='reviews.app')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL)),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='assigned_reviews', to=settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True})),
            ],
        ),
    ]
