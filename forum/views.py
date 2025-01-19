from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.db.models import Q
from django.core.cache import cache

from rest_framework import generics, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination



from drf_yasg.utils import swagger_auto_schema

from .models import Profile, category, question, answer, commentAnswer, likesAnswer

from .serializers import (
    ProfileSerializer, 
    CategorySerializer,
    QuestionSerializer,
    AnswerSerializer,
    LikesAnswerSerializer,
    CommentSerializer
    )

from .forms import (
    QuestionForm,
    UpdateQuestionForm,
    QuestionCreateForm,
)

from .filter import QuestionFilter, AnswerFilter, LikesAnswerFilter

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    @action(methods=["get"], detail=False)
    def profile_filter(self, request):
        filter_account = Q(user__email__contains="gmail") & (
            ~Q(user__username="admin") | Q(user__first_name="Сергей")
        )

        filtred_profiles = Profile.objects.filter(filter_account)
        serializer = ProfileSerializer(filtred_profiles, many=True)
        return Response(serializer.data)


# class questionViewSet(viewsets.ReadOnlyModelViewSet):
# queryset = question.objects.all()
# serializer_class = questionSerializer
# filter_backends = [DjangoFilterBackend, SearchFilter]
# search_fields = ['question_title','question_body']
# filterset_class = questionFilter

# @action(methods=['get'], detail=False)
# def question_filter(self,request):
#     filterQuestion = (
#         ~Q(user='1') &
#         (Q(category='1') | Q(category='4'))
#     )

#     filtredQuestions = question.objects.filter(filterQuestion).exclude(user='2')
#     serializer = questionSerializer(filtredQuestions, many=True)
#     return Response(serializer.data)

# @action(methods=['post', 'get'], detail=True)
# def changeQuestion(self, request, pk=None):
#     question = self.get_object()
#     serializer = self.get_serializer(question, data=request.data, partial=True)
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data)
#     else:
#         return Response(serializer.errors)

class QuestionViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = question.objects.all()
    serializer_class = QuestionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["question_title", "question_body"]
    filterset_class = QuestionFilter
    """
    API endpoint для работы с вопросами
    """

    @swagger_auto_schema(
        operation_description="Получить список всех вопросов",
        responses={200: QuestionSerializer(many=True)},
    )
    def list(self, request):
        return super().list(request)

    @swagger_auto_schema(
        operation_description="Получить детальную информацию о вопросе",
        responses={200: QuestionSerializer, 404: "Вопрос не найден"},
    )
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)


class QuestionDelete(generics.RetrieveDestroyAPIView):
    """ удаление вопроса в апишке """
    queryset = question.objects.all()
    serializer_class = QuestionSerializer


class QuestionCreate(generics.ListCreateAPIView):
    """ создание вопроса в апишке """
    queryset = question.objects.all()
    serializer_class = QuestionSerializer


class CategoryViewSetPagination(PageNumberPagination):
    """ пагинация для категорий """
    page_size = 3
    page_size_query_param = "page_size"
    max_page_size = 5


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ список категорий """
    queryset = category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = CategoryViewSetPagination


class AnswerApiUpdate(generics.UpdateAPIView):
    """ изменение ответа в апи """
    queryset = answer.objects.all()
    serializer_class = AnswerSerializer


class AnswerViewSet(viewsets.ReadOnlyModelViewSet):
    """ список всех ответов в апи """
    queryset = answer.objects.order_by("-answer_date")
    serializer_class = AnswerSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = [
        "answer_body",
    ]
    filterset_class = AnswerFilter

    @action(methods=["get"], detail=True)
    def like(self, request):
        user = None
        if request and hasattr(request, "user"):
            user = request.user
        profile = get_object_or_404(Profile, user=user)
        answer = self.get_object()
        likesAnswer.objects.get_or_create(user=profile, answer=answer)
        return Response(status=status.HTTP_201_CREATED)


class CommentViewSet(viewsets.ReadOnlyModelViewSet):
    """ список комментариев в апи """
    queryset = commentAnswer.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ["comment_body"]


class LikesAnswers(viewsets.ReadOnlyModelViewSet):
    """ список лайко в апи """
    queryset = likesAnswer.objects.all()
    serializer_class = LikesAnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LikesAnswerFilter


def index(request):
    """ вывод на страницу index """
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("forum/succesCreateQuestion")
    context = {"form": form}
    return render(request, "forum/index.html", context)


def answer_detail(request, answer_id):
    """ содержание ответа """
    answerdet = get_object_or_404(answer, pk=answer_id)
    context = {
        "answerdet": answerdet,
    }
    return render(request, "forum/answer_detail.html", context)


def last_question(request):
    """ вывод последнего вопроса из бд """
    last_question_def = list(question.objects.all())
    return render(request, "forum/last_question.html", {"lastQuestion": last_question_def})


def succes_create_question(request):
    """ страница после успешного добавления вопроса """
    return render(request, "forum/succesCreateQuestion.html", {})


def all_questions(request):
    """ список всех вопросов с категориями """
    questions = question.objects.select_related("category").all()
    return render(request, "forum/all_questions.html", {"questions": questions})


def user_questions(request):
    """ вывод всех вопросов каждого пользователя """
    users = Profile.objects.prefetch_related("questions_by").all()
    count_questions_all = question.objects.count()
    context = {"users": users, "count": count_questions_all}
    return render(request, "forum/user_questions.html", context)


def categories(request):
    """ список всех категорий """
    categories_def = category.objects.values("category_name", "category_image")
    return render(request, "forum/categories.html", {"categories": categories_def})


def filtered_questions(request):
    """ вывод вопросов после 2025 года """
    current_year = timezone.now().year
    questions = question.objects.filter(
        question_date__gt=timezone.datetime(current_year, 1, 1)
    ).filter(user="1")
    return render(request, "forum/filtered_questions.html", {"questions": questions})


def question_contains_word(request):
    """ проферка функции contains """
    question_contains_word_def = question.objects.filter(
        question_body__contains="Университет"
    )
    return render(
        request,
        "forum/question_contains_word.html",
        {"questions": question_contains_word_def},
    )


def question_icontains_word(request):
    """ проферка функции icontains """
    question_icontains_word_def = question.objects.filter(
        question_body__icontains="велосипед"
    )
    return render(
        request,
        "forum/question_icontains_word.html",
        {"questions": question_icontains_word_def},
    )


def questions_with_answers_count(request):
    """ посчет ответов на вопросы """
    questions = question.objects.all()
    questions_with_counts = []
    for q in questions:
        has_answers = q.answers.exists()
        answers_count = q.answers.count()
        questions_with_counts.append(
            {"question": q, "has_answers": has_answers, "answers_count": answers_count}
        )
    context = {"questions_with_counts": questions_with_counts}
    return render(request, "your_template.html", context)


def update_question(request, question_id):
    """ изменение вопроса """
    question_update = question.objects.get(id=question_id)

    if request.method == "POST":
        form = UpdateQuestionForm(request.POST, instance=question_update)
        if form.is_valid():
            question.objects.filter(pk=question_id).update(**form.cleaned_data)
            return redirect("manage_question", question_id=question_id)
    else:
        form = UpdateQuestionForm(instance=question_update)

    return render(request, "forum/update_question.html", {"form": form})


def delete_question(question_id):
    """ удаление вопроса """
    try:
        question.objects.get(id=question_id).delete()
        return True, "Вопрос успешно удалён."
    except question.objects.get(id=question_id).DoesNotExist:
        return False, "Вопрос не найден."


def manage_question(request, question_id):
    """ форма удаления или изменения вопроса """
    question_obj = get_object_or_404(question, id=question_id)

    # Проверяем, является ли пользователь автором вопроса
    is_author = request.user == question_obj.user

    if request.method == "POST":

        action_def = request.POST.get("action")

        if action_def == "delete":
            question_obj.delete()
            return redirect("main_page")

        if action_def == "edit":
            return redirect("update_question", question_id=question_id)

    return render(
        request,
        "forum/question_detail.html",
        {
            "question": question_obj,
            "is_author": is_author,
        },
    )


def create_question_view(request):
    """ создание вопроса """
    if request.method == "POST":
        form = QuestionCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("forum/succesCreateQuestion")
    else:
        form = QuestionCreateForm()
    return render(request, "forum/create_question.html", {"form": form})


def main_page(request):
    """ главная страница сайта """
    categories_for = category.objects.all()

    last_questions_def = cache.get('last_questions_cache')
    if not last_questions_def:
        print("Данные извлекаются из базы данных")
        last_questions_def = question.objects.prefetch_related("user")[0:5]
        cache.set('last_questions_cache', last_questions_def, timeout=60 * 10)
    else:
        print("Данные получены из кэша")
    search_query = request.GET.get("search", "")
    search_results = None
    if search_query:
        search_results = question.objects.filter(
            Q(question_title__icontains=search_query)
            | Q(question_body__icontains=search_query)
        ).order_by("-id")

    return render(
        request,
        "forum/main_page.html",
        {
            "categories": categories_for,
            "lastQuestions": last_questions_def,
            "search_query": search_query,
            "search_results": search_results,
            "search_query": search_query,
        },
    )

