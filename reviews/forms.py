from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    text = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 5000, 'rows':6}), required=True)

    class Meta:
        model = Review
        fields = ['text','sentiment','sentiment_polarity','sentiment_subjectivity']
