from django.forms import ModelForm, ModelForm, TextInput, Select, Textarea
from .models import question

class questionForm(ModelForm):
    class Meta:
        model = question
        fields = ['category', 'user', 'question_title', 'question_body']
        widgets = {
            'category': Select(attrs={'class': 'form-control'}),
            'user': Select(attrs={'class': 'form-control'}),
            'question_title': TextInput(attrs={'class': 'form-control'}),
            'question_body': Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }