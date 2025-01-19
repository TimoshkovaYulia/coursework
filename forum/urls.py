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

from django.conf import settings
from django.conf.urls.static import static

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
    path("createQuestion", views.index, name="index"),
    path("test/<int:answer_id>", views.answer_detail, name="detail"),
    path("lastQuestion", views.last_question, name="lastQuestion"),
    path("forum/succesCreateQuestion", views.succesCreateQuestion, name="succes"),
    path("all_questions", views.all_questions, name="all_questions"),
    path("user_questions", views.user_questions, name="user_questions"),
    path("categories", views.categories, name="categories"),
    path("filtered_questions", views.filtered_questions, name="filtered_questions"),
    path("question_contains_word", views.question_contains_word, name="question_contains_word"),
    path("question_icontains_word", views.question_icontains_word, name="question_icontains_word"),
    path("manage_question", views.manage_question, name="manage_question"),
    path("update_question/<int:question_id>/", views.update_question, name="update_question"),
    path("last_question", views.last_question, name="last_question"),
    path('create_question', views.create_question_view, name='create_question'),
    path('main_page', views.main_page, name='main_page'),
]