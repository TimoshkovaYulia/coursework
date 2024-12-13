from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import question, category, answer, commentAnswer, likesAnswer, likesComment, Profile
from import_export.admin import ExportActionModelAdmin
from import_export import resources
from googletrans import Translator

@admin.register(Profile)
class profileAdmin(admin.ModelAdmin):
    list_display = ['user', 'user__email']

class categoryResource(resources.ModelResource):
    
    class Meta:
        model = category
        fields = ('category_name',)

    def get_category(self, obj):
        return f"Категория: {obj.category_name}"

    def dehydrate_category_name(self, obj):
        return self.get_category(obj)


@admin.register(category)
class categoryAdmin(ExportActionModelAdmin, SimpleHistoryAdmin):
    list_display = ['category_name', 'questions_count']
    resource_class = categoryResource


class questionResource(resources.ModelResource):

    class Meta:
        model = question
        fields = ('user', 'category', 'question_title','question_date')
        


@admin.register(question)
class questionAdmin(ExportActionModelAdmin, SimpleHistoryAdmin):
    resource_class = questionResource
    list_filter = ["category", "question_date"]
    list_display = ['user', 'category', 'question_title','question_date']
    search_fields = ('question_title','question_date')
    fields = ['user', 'category', 'question_title']

    def get_export_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(category__id = 1)




class answerResource(resources.ModelResource):
    def dehydrate_answer_body(self, answer:'answer'):
        return answer.answer_body.upper()
    
    def dehydrate_user_answer(self, answer:'answer'):
        return answer.user_answer.user.username
    def dehydrate_question(self, answer:'answer'):
        return answer.question.question_body
    
    class Meta:
        model = answer
        fields = ('user_answer', 'answer_body','question')


@admin.register(answer)
class answerAdmin(ExportActionModelAdmin, SimpleHistoryAdmin):
    resource_class = answerResource
    list_display = ['user_answer', 'question__question_title', 'answer_body', 'answer_date']
    list_filter = ["user_answer", "answer_date"]




@admin.register(commentAnswer)

class commentAdmin(SimpleHistoryAdmin):
    list_display = ['user', 'comment_body']


class likesAnswerResource(resources.ModelResource):

    def get_user(self, LikesAnswer: 'likesAnswer'):
        return f"Пользователь: {LikesAnswer.user.username}"
    
    class Meta:
        model = likesAnswer
        fields = ('user', 'answer')


@admin.register(likesAnswer)

class likesAnswerAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    resource_class = likesAnswerResource
    list_display = ['user', 'answer']

@admin.register(likesComment)

class likesCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'comment']