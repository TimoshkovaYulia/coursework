from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import generics, viewsets
from .models import Profile
from .models import category
from .models import question
from .models import answer
from .models import commentAnswer
from .models import likesAnswer

from django.utils import timezone

from .serializers import profileSerializer
from .serializers import categorySerializer
from .serializers import questionSerializer
from .serializers import answerSerializer
from .serializers import commentSerializer, likesAnswerSerializer

from .forms import questionForm, questionSelectionForm, updateQuestionForm, QuestionCreateForm

from django.shortcuts import redirect
from django.http import HttpResponseRedirect

from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from .filter import questionFilter
from .filter import answerFilter, likesAnswerFilter
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status

from drf_yasg.utils import swagger_auto_schema

class profileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = profileSerializer

    @action(methods=['get'], detail=False)
    def profile_filter(self,request):
        filterAccount = (
            Q(user__email__contains='gmail') &
            (~Q(user__username='admin') | Q(user__first_name='Сергей'))
        )

        filtredProfiles = Profile.objects.filter(filterAccount)
        serializer = profileSerializer(filtredProfiles, many=True)
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

from drf_yasg.utils import swagger_auto_schema

class questionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = question.objects.all()
    serializer_class = questionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['question_title','question_body']
    filterset_class = questionFilter
    """
    API endpoint для работы с вопросами
    """
    @swagger_auto_schema(
        operation_description="Получить список всех вопросов",
        responses={200: questionSerializer(many=True)}
    )
    def list(self, request):
        return super().list(request)

    @swagger_auto_schema(
        operation_description="Получить детальную информацию о вопросе",
        responses={
            200: questionSerializer,
            404: "Вопрос не найден"
        }
    )
    def retrieve(self, request, pk=None):
        return super().retrieve(request, pk)

class questionDelete(generics.RetrieveDestroyAPIView):
    queryset = question.objects.all()
    serializer_class = questionSerializer

class questionCreate(generics.ListCreateAPIView):
    queryset = question.objects.all()
    serializer_class = questionSerializer

class categoryViewSetPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'
    max_page_size = 5

class categoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = category.objects.all()
    serializer_class = categorySerializer
    pagination_class = categoryViewSetPagination


class answerApiUpdate(generics.UpdateAPIView):
    queryset = answer.objects.all()
    serializer_class = answerSerializer


class answerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = answer.objects.order_by('-answer_date')
    serializer_class = answerSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['answer_body',]
    filterset_class = answerFilter

    @action(methods=['get'], detail=True)
    def like(self, request, pk=None):
        user = None
        if request and hasattr(request, "user"):
            user = request.user
        profile = get_object_or_404(Profile, user=user)
        answer = self.get_object()
        likesAnswer.objects.get_or_create(user=profile, answer=answer)
        return Response(status=status.HTTP_201_CREATED)

class commentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = commentAnswer.objects.all()
    serializer_class = commentSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['comment_body']


class likesAnswers(viewsets.ReadOnlyModelViewSet):
    queryset = likesAnswer.objects.all()
    serializer_class = likesAnswerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = likesAnswerFilter

def index(request):
    form = questionForm()

    if request.method == 'POST':
        form = questionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('forum/succesCreateQuestion')
    context = {'form': form}
    return render(request, 'forum/index.html', context)
    
def answer_detail(request, answer_id):
    answerdet = get_object_or_404(answer, pk=answer_id)
    context = {
        'answerdet': answerdet,
    }
    return render(request, 'forum/answer_detail.html', context)

def last_question(request):
    lastQuestion = list(question.objects.all())
    return render(request, 'forum/last_question.html', {'lastQuestion': lastQuestion})


def succesCreateQuestion(request):
    return render(request, 'forum/succesCreateQuestion.html', {})

def all_questions(request):
    questions = question.objects.select_related('category').all()
    return render(request, 'forum/all_questions.html', {'questions': questions})

def user_questions(request):
    users = Profile.objects.prefetch_related('questions_by').all()
    count_questions_all = question.objects.count()
    context = {
        'users': users,
        'count': count_questions_all
    }
    return render(request, 'forum/user_questions.html', context)

def categories(request):
    categories = category.objects.values('category_name', 'category_image')
    return render(request, 'forum/categories.html', {'categories': categories})

def filtered_questions(request):
    current_year = timezone.now().year
    questions = question.objects.filter(question_date__gt=timezone.datetime(current_year, 1, 1)).filter(user="1")
    return render(request, "forum/filtered_questions.html", {"questions": questions})

def question_contains_word(request):
    question_contains_word = question.objects.filter(question_body__contains = 'Университет')
    return render(request, "forum/question_contains_word.html", {"questions": question_contains_word})

def question_icontains_word(request):
    question_icontains_word = question.objects.filter(question_body__icontains = 'велосипед')
    return render(request, "forum/question_icontains_word.html", {"questions": question_icontains_word})

def questions_with_answers_count(request):
    questions = question.objects.all()
    questions_with_counts = []
    for q in questions:
        has_answers = q.answers.exists()
        answers_count = q.answers.count()
        questions_with_counts.append({
            'question': q,
            'has_answers': has_answers,
            'answers_count': answers_count
        })
    context = {
        'questions_with_counts': questions_with_counts
    }
    return render(request, 'your_template.html', context)

def update_question(request, question_id):
    question_update = question.objects.get(id=question_id)
    
    if request.method == 'POST':
        form = updateQuestionForm(request.POST, instance=question_update)
        if form.is_valid():
            question.objects.filter(pk=question_id).update(**form.cleaned_data)
            return redirect('manage_question', question_id=question_id)
    else:
        form = updateQuestionForm(instance=question_update)
    
    return render(request, 'forum/update_question.html', {'form': form})

def delete_question(question_id):
    try:
        question.objects.get(id=question_id).delete()
        return True, "Вопрос успешно удалён."
    except question.objects.get(id=question_id).DoesNotExist:
        return False, "Вопрос не найден."

def manage_question(request, question_id):
    question_obj = get_object_or_404(question, id=question_id)
    
    # Проверяем, является ли пользователь автором вопроса
    is_author = request.user == question_obj.user
    
    if request.method == 'POST':
                   
        action = request.POST.get('action')
        
        if action == 'delete':
            question_obj.delete()
            return redirect('main_page')
            
        elif action == 'edit':
            return redirect('update_question', question_id=question_id)
    
    return render(request, 'forum/question_detail.html', {
        'question': question_obj,
        'is_author': is_author,
    })


def create_question_view(request):
    if request.method == 'POST':
        form = QuestionCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('forum/succesCreateQuestion')
    else:
        form = QuestionCreateForm()
    return render(request, 'forum/create_question.html', {'form': form})

def main_page(request):
    categories = category.objects.all()
    lastQuestions = question.objects.prefetch_related('user')[0:5]
    search_query = request.GET.get('search', '')
    search_results = None
    if search_query:
        search_results = question.objects.filter(
            Q(question_title__icontains=search_query) |
            Q(question_body__icontains=search_query)
        ).order_by("-id")

    return render(request, 'forum/main_page.html', {
        'categories': categories,
        'lastQuestions': lastQuestions,
        'search_query': search_query,
        'search_results': search_results,
        'search_query': search_query,
    })
