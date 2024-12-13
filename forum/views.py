from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, viewsets
from .models import Profile
from .models import category
from .models import question
from .models import answer
from .models import commentAnswer
from .models import likesAnswer
from .models import likesComment

from .serializers import profileSerializer
from .serializers import categorySerializer
from .serializers import questionSerializer
from .serializers import answerSerializer
from .serializers import commentSerializer, likesAnswerSerializer

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
    
    

class questionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = question.objects.all()
    serializer_class = questionSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['question_title','question_body']
    filterset_class = questionFilter
    

    @action(methods=['get'], detail=False)
    def question_filter(self,request):
        filterQuestion = (
            ~Q(user='1') &
            (Q(category='1') | Q(category='4'))
        )

        filtredQuestions = question.objects.filter(filterQuestion)
        serializer = questionSerializer(filtredQuestions, many=True)
        return Response(serializer.data)
    
    @action(methods=['post', 'get'], detail=True)
    def changeQuestion(self, request, pk=None):
        question = self.get_object()
        serializer = self.get_serializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

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
    queryset = answer.objects.all()
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
    return render(request, 'forum/index.html', {})
    
