from django import forms
from festival.models import Voice, Request

class VoteForm(forms.ModelForm):

    class Meta:
        model = Voice
        # voice = forms.CharField()
        fields = ['voice']
