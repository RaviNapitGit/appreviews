from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


class App(models.Model):
    APP_TYPE_CHOICES = [('Free', 'Free'), ('Paid', 'Paid')]

    name = models.CharField(max_length=255, unique=True, db_index=True)
    category = models.CharField(max_length=128)
    rating = models.FloatField(null=True)
    reviews_count = models.IntegerField(default=0)
    size = models.CharField(max_length=64, null=True, blank=True)
    installs = models.IntegerField(default=0, db_index=True)
    app_type = models.CharField(max_length=8, choices=APP_TYPE_CHOICES, default='Free')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    content_rating = models.CharField(max_length=64, null=True, blank=True)
    genres = models.CharField(max_length=255, null=True, blank=True)
    last_updated = models.DateField(null=True, blank=True)
    current_ver = models.CharField(max_length=64, null=True, blank=True)
    android_ver = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    SENTIMENT_CHOICES = [('Positive', 'Positive'), ('Neutral', 'Neutral'), ('Negative', 'Negative')]
    STATUS_CHOICES = [('PENDING', 'PENDING'), ('APPROVED', 'APPROVED'), ('REJECTED', 'REJECTED')]

    app = models.ForeignKey(App, on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    supervisor = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL,
                                   limit_choices_to={'is_staff': True}, related_name='assigned_reviews')
    text = models.TextField()
    sentiment = models.CharField(max_length=8, choices=SENTIMENT_CHOICES, null=True, blank=True)
    sentiment_polarity = models.FloatField(null=True, blank=True)
    sentiment_subjectivity = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='PENDING', db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def approve(self, supervisor_user):
        self.status = 'APPROVED'
        self.approved_at = timezone.now()
        self.supervisor = supervisor_user
        self.save()


# Simple key-value to persist last assigned supervisor for round-robin
class KeyValue(models.Model):
    key = models.CharField(max_length=128, unique=True)
    value = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.key}={self.value}"
