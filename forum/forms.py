from django.forms import ModelForm, ModelForm, TextInput, Select, Textarea
from .models import question
from django import forms

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


class questionSelectionForm(forms.Form):
    question_choices = [(q.id, q.question_title) for q in question.objects.all()]
    selected_question = forms.ChoiceField(label="Выберите вопрос:", choices=question_choices)
    action = forms.ChoiceField(
        label="Действие:",
        choices=[
            ("update", "Обновить"),
            ("delete", "Удалить"),
        ],
        widget=forms.RadioSelect,
    )

class updateQuestionForm(forms.ModelForm):
    class Meta:
        model = question
        fields = ['question_title', 'question_body']
        widgets = {
            
            'question_title': TextInput(attrs={'class': 'form-control'}),
            'question_body': Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }


class QuestionCreateForm(forms.ModelForm):
    class Meta:
        model = question
        fields = ['user','category', 'question_title', 'question_body', 'document']
        labels = {
            'document': ('Загрузите документ'),
        }
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'question_title': forms.TextInput(attrs={'class': 'form-control'}),
            'question_body': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
        }