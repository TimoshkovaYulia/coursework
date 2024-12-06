from django.urls import path, include
from rest_framework.routers import DefaultRouter

from forum.views import profileViewSet
from forum.views import categoryViewSet
from forum.views import questionViewSet
from forum.views import answerViewSet
from forum.views import commentViewSet

from . import views



router = DefaultRouter()
router.register(r'profiles', profileViewSet, basename='profileAccount')
router.register(r'categories', categoryViewSet, basename='category')
router.register(r'question', questionViewSet, basename='question')
router.register(r'answers', answerViewSet, basename='answer')
router.register(r'comments', commentViewSet, basename='commentAnswer')

urlpatterns = [
    path('', include(router.urls)),
    path("", views.index, name="index"),

]