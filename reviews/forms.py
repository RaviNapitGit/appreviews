from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    # Only expose the text field to users (sentiment fields are collected elsewhere / via import)
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'maxlength': 5000,
            'rows': 6,
            'class': 'form-control',
            'placeholder': 'Write your review here...'
        }),
        required=True,
        label='Your review'
    )

    class Meta:
        model = Review
        # Only include text for user-submitted reviews
        fields = ['text']
