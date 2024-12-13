from django.urls import path, include
from rest_framework.routers import DefaultRouter

from forum.views import profileViewSet
from forum.views import categoryViewSet
from forum.views import questionViewSet
from forum.views import answerApiUpdate
from forum.views import questionDelete
from forum.views import questionCreate
from forum.views import answerViewSet
from forum.views import commentViewSet, likesAnswers

from . import views



router = DefaultRouter()
router.register(r'profiles', profileViewSet, basename='Profile')
router.register(r'categories', categoryViewSet, basename='category')
router.register(r'question', questionViewSet, basename='question')
router.register(r'answers', answerViewSet, basename='answer')
router.register(r'comments', commentViewSet, basename='commentAnswer')
router.register(r'likesAnswer', likesAnswers, basename='likesAnswer')



urlpatterns = [
    path('answerUpdate/<int:pk>', answerApiUpdate.as_view()),
    path('questionCreate/', questionCreate.as_view()),
    path('questionDelete/<int:pk>', questionDelete.as_view()),
    path('', include(router.urls)),
    path("", views.index, name="index"),

]