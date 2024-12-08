from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics, viewsets
from .models import profileAccount
from .models import category
from .models import question
from .models import answer
from .models import commentAnswer
from .serializers import profileSerializer
from .serializers import categorySerializer
from .serializers import questionSerializer
from .serializers import answerSerializer
from .serializers import commentSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination

from django.db.models import Q

class profileViewSet(viewsets.ModelViewSet):
    queryset = profileAccount.objects.all()
    serializer_class = profileSerializer

    @action(methods=['get'], detail=False)
    def profile_filter(self,request):
        filterAccount = (
            ~Q(email__contains='mail') &
            (Q(user_name__contains='Иванов') | Q(user_name__contains='Валерия'))
        )

        filtredProfiles = profileAccount.objects.filter(filterAccount)
        serializer = profileSerializer(filtredProfiles, many=True)
        return Response(serializer.data)
    
    

class questionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = question.objects.all()
    serializer_class = questionSerializer

    @action(methods=['get'], detail=False)
    def question_filter(self,request):
        filterQuestion = (
            ~Q(id_user='1') &
            (Q(id_category='1') | Q(id_category='4'))
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
    
    filter_backends = [DjangoFilterBackend]
    filter_fields = ['question_body']

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

class commentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = commentAnswer.objects.all()
    serializer_class = commentSerializer

def index(request):
    return render(request, 'forum/index.html', {})
    
