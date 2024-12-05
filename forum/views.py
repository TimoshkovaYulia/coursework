from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import generics
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


class profileApiView(generics.ListAPIView):
    queryset = profileAccount.objects.all()
    serializer_class = profileSerializer

class categoryApiView(generics.ListAPIView):
    queryset = category.objects.all()
    serializer_class = categorySerializer

class questionApiView(generics.ListAPIView):
    queryset = question.objects.all()
    serializer_class = questionSerializer

class answerApiView(generics.ListAPIView):
    queryset = answer.objects.all()
    serializer_class = answerSerializer

class commentApiView(generics.ListAPIView):
    queryset = commentAnswer.objects.all()
    serializer_class = commentSerializer

def index(request):
    return render(request, 'forum/index.html', {})
    