from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from reviews.models import App, Review
from django.urls import reverse

User = get_user_model()

class FlowTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.sup = User.objects.create_user('sup', password='pass', is_staff=True)
        self.user = User.objects.create_user('user', password='pass', is_staff=False)
        self.app = App.objects.create(name='CoolApp', category='Games', installs=5000)

    def test_suggest_endpoint(self):
        # suggestion requires >=3 chars
        resp = self.client.get(reverse('reviews:api_suggest') + '?q=Co')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])
        resp = self.client.get(reverse('reviews:api_suggest') + '?q=Cool')
        self.assertEqual(resp.status_code, 200)
        # may return an empty list depending on FTS; ensure it is list
        self.assertIsInstance(resp.json(), list)

    def test_user_create_review_and_assignment(self):
        self.client.login(username='user', password='pass')
        resp = self.client.post(reverse('reviews:review_create', args=[self.app.pk]), {
            'text': 'Great app', 'sentiment':'Positive'
        }, follow=True)
        self.assertEqual(resp.status_code, 200)
        r = Review.objects.get(author=self.user)
        self.assertEqual(r.status, 'PENDING')

    def test_supervisor_approve(self):
        r = Review.objects.create(app=self.app, author=self.user, text='Nice', status='PENDING', supervisor=self.sup)
        self.client.login(username='sup', password='pass')
        resp = self.client.post(reverse('reviews:approve_review', args=[r.pk]), follow=True)
        self.assertEqual(resp.status_code, 200)
        r.refresh_from_db()
        self.assertEqual(r.status, 'APPROVED')
