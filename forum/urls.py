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

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

from django.conf import settings
from django.conf.urls.static import static

from . import views



router = DefaultRouter()
router.register(r'profiles', profileViewSet, basename='Profile')
router.register(r'categories', categoryViewSet, basename='category')
router.register(r'questionn', questionViewSet, basename='question')
router.register(r'answers', answerViewSet, basename='answer')
router.register(r'comments', commentViewSet, basename='commentAnswer')
router.register(r'likesAnswer', likesAnswers, basename='likesAnswer')

schema_view = get_schema_view(
    openapi.Info(
        title="Forum API",
        default_version='v1',
        description="API документация для форума вопросов и ответов",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@forum.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),

)

urlpatterns = [
    path('answerUpdate/<int:pk>', answerApiUpdate.as_view()),
    path('questionCreate/', questionCreate.as_view()),
    path('questionDelete/<int:pk>', questionDelete.as_view()),
    # path('', include(router.urls)),
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
    # path("manage_question/", views.manage_question, name="manage_question"),
    path("update_question/<int:question_id>/", views.update_question, name="update_question"),
    path("last_question", views.last_question, name="last_question"),
    path('create_question', views.create_question_view, name='create_question'),
    path('', views.main_page, name='main_page'),
    path('question/<int:question_id>/', views.manage_question, name='manage_question'),
    path('answer_detail/<int:answer_id>', views.answer_detail, name='answer_detail'),
    
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]