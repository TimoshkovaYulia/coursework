from django_filters import rest_framework as filters
from .models import answer
from .models import question, likesAnswer


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass

class questionFilter(filters.FilterSet):

    class Meta:
        model = question
        fields = ['category', 'user']

class answerFilter(filters.FilterSet):
    answer_date = filters.DateFilter(label='Дата публикации')

    class Meta:
        model = answer
        fields = ['answer_date', 'question']

class likesAnswerFilter(filters.FilterSet):

    class Meta:
        model = likesAnswer
        fields = ['user']


