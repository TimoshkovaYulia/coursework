from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from import_export.admin import ExportActionModelAdmin
from import_export import resources

from .models import question, category, answer, commentAnswer, likesAnswer, Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    '''ffr'''
    list_display = ["user", "user__email"]


class CategoryResource(resources.ModelResource):
    ''' категории админ '''
    class Meta:
        model = category
        fields = ("category_name",)

    def get_category(self, obj):
        return f"Категория: {obj.category_name}"

    def dehydrate_category_name(self, obj):
        return self.get_category(obj)


@admin.register(category)
class CategoryAdmin(ExportActionModelAdmin, SimpleHistoryAdmin):
    ''' категории '''
    list_display = ["category_name", "questions_count", "category_image"]
    resource_class = CategoryResource


class QuestionResource(resources.ModelResource):
    '''  '''
    class Meta:
        model = question
        fields = ("user", "category", "question_title", "question_date")


class QuestionInline(admin.TabularInline):
    '''  '''
    model = answer
    raw_id_fields = ["question"]


@admin.register(question)
class QuestionAdmin(ExportActionModelAdmin, SimpleHistoryAdmin):
    ''' c '''
    resource_class = QuestionResource
    list_filter = ["category", "question_date"]
    list_display = [
        "user",
        "category",
        "question_title",
        "question_date",
        "question_time",
        "document",
    ]
    search_fields = ("question_title", "question_date")
    fields = [
        "user",
        "category",
        "question_title",
        "question_body",
        "question_date",
        "question_time",
        "document",
    ]
    readonly_fields = ("question_date", "question_time")
    inlines = [QuestionInline]
    list_display_links = ["category", "question_title"]

    def get_export_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(category__id=1)

class AnswerResource(resources.ModelResource):
    ''' s '''
    def dehydrate_answer_body(self, answer: "answer"):
        return answer.answer_body.upper()

    def dehydrate_user_answer(self, answer: "answer"):
        return answer.user_answer.user.username

    def dehydrate_question(self, answer: "answer"):
        return answer.question.question_body

    class Meta:
        model = answer
        fields = ("user_answer", "answer_body", "question", "source_url")


@admin.register(answer)
class AnswerAdmin(ExportActionModelAdmin, SimpleHistoryAdmin):
    ''' s '''
    resource_class = AnswerResource
    list_display = [
        "user_answer",
        "question__question_title",
        "answer_body",
        "source_url",
    ]
    list_filter = ["user_answer", "answer_date"]
    # actions = [generate_pdf]
    date_hierarchy = "answer_date"


@admin.register(commentAnswer)
class CommentAdmin(SimpleHistoryAdmin):
    ''' s '''
    list_display = ["user", "comment_body", "like_count"]
    filter_horizontal = ("likes",)

    @admin.display(description="Количество лайков")
    def like_count(self, obj):
        return obj.likes.count()


class LikesAnswerResource(resources.ModelResource):
    ''' d '''
    def get_user(self, LikesAnswer: "likesAnswer"):
        return f"Пользователь: {LikesAnswer.user.username}"

    class Meta:
        model = likesAnswer
        fields = ("user", "answer")


@admin.register(likesAnswer)
class LikesAnswerAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    ''' s '''
    resource_class = LikesAnswerResource
    list_display = ["user", "answer"]

