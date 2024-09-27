from django import forms
from .models import Movie, Reple

class MovieForm(forms.ModelForm):
    title = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'ex) 부산행 (Train to Busan)',
            }
        )
    )
    content = forms.CharField(
        label = 'Description',
        widget= forms.Textarea(
            attrs={
                'class' : 'form-control',
                'placeholder' : 'ex) 좀비 바이러스가 퍼진 한국에서, 한 가족과 승객들이 기차 안에서 생존을 위해 싸우는 이야기를 그린 스릴러입니다.',
            }
        )
    )
    class Meta:
        model = Movie
        fields = '__all__'

class RepleForm(forms.Form):
    class Meta:
        model = Reple
        fields = '__all__'