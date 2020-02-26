from django import forms  
from users.models import UserProfile  
  
  
class ProfileCreationForm(forms.ModelForm):  
  
    class Meta:  
        model = UserProfile  
        fields = ['info']