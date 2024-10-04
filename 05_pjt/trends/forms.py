from django import forms
from .models import Keyword

class KeywordForm(forms.ModelForm):
    name = forms.CharField()
    
    class Meta:
        model = Keyword
        fields = '__all__'
        