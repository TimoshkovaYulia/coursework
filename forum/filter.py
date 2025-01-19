from django_filters import rest_framework as filters
from .models import answer
from .models import question, likesAnswer


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class QuestionFilter(filters.FilterSet):
    ''' фильтр вопросов '''
    class Meta:
        model = question
        fields = ["category", "user"]


class AnswerFilter(filters.FilterSet):
    ''' фильтр ответов '''
    answer_date = filters.DateFilter(label="Дата публикации")

    class Meta:
        model = answer
        fields = ["answer_date", "question"]


class LikesAnswerFilter(filters.FilterSet):
    ''' фильтр лайков на ответ '''
    class Meta:
        model = likesAnswer
        fields = ["user"]
