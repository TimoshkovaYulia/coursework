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
from django.db.models import Q

class profileViewSet(viewsets.ModelViewSet):
    queryset = profileAccount.objects.all()
    serializer_class = profileSerializer

    @action(methods=['get'], detail=False)
    def profile_filter(self,request):
        print(0)
        filterAccount = (
            ~Q(email__contains='mail') &
            (Q(user_name__contains='Иванов') | Q(user_name__contains='Валерия'))
        )

        filtredProfiles = profileAccount.objects.filter(filterAccount)
        serializer = profileSerializer(filtredProfiles, many=True)
        return Response(serializer.data)

class questionViewSet(viewsets.ModelViewSet):
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

class categoryViewSet(viewsets.ModelViewSet):
    queryset = category.objects.all()
    serializer_class = categorySerializer

class answerViewSet(viewsets.ModelViewSet):
    queryset = answer.objects.all()
    serializer_class = answerSerializer

class commentViewSet(viewsets.ModelViewSet):
    queryset = commentAnswer.objects.all()
    serializer_class = commentSerializer

def index(request):
    return render(request, 'forum/index.html', {})
    