from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin
from .models import question, category, answer, commentAnswer, likesAnswer, Profile
from import_export.admin import ExportActionModelAdmin
from import_export import resources

import io
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont

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
    list_display = ['category_name', 'questions_count', 'category_image']
    resource_class = categoryResource


class questionResource(resources.ModelResource):
    class Meta:
        model = question
        fields = ('user', 'category', 'question_title','question_date')
        
class questionInline(admin.TabularInline):
    model = answer
    raw_id_fields = ['question']

@admin.register(question)
class questionAdmin(ExportActionModelAdmin, SimpleHistoryAdmin):
    resource_class = questionResource
    list_filter = ["category", "question_date"]
    list_display = ['user', 'category', 'question_title', 'question_date','question_time', 'document']
    search_fields = ('question_title','question_date')
    fields = ['user', 'category', 'question_title', 'question_body','question_date', 'question_time', 'document']
    readonly_fields = ('question_date', 'question_time')
    inlines = [questionInline]
    list_display_links = ['category', 'question_title']


    def get_export_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.filter(category__id = 1)

pdfmetrics.registerFont(TTFont('LTSuperior-Regular', 'C:/Users/utimo/Desktop/институт лиф/5 семестр/web/djangoproject/venv/Lib/site-packages/reportlab/fonts/LTSuperior-Regular.ttf'))
def generate_pdf(modeladmin, request, queryset):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    
    p.setFont('LTSuperior-Regular', 12)
    p.translate(inch, 9*inch)
    
    for obj in queryset:
        p.drawString(0, 0, f'user: {obj.user_answer}')
        p.drawString(0, -10, f'Вопрос: {obj.question.question_body}')
        p.drawString(0, -20, f'Ответ: {obj.answer_body}')
        p.showPage()
    
    p.save()
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')
generate_pdf.short_description = "Создать PDF файл"


class answerResource(resources.ModelResource):
    def dehydrate_answer_body(self, answer:'answer'):
        return answer.answer_body.upper()
    
    def dehydrate_user_answer(self, answer:'answer'):
        return answer.user_answer.user.username
    def dehydrate_question(self, answer:'answer'):
        return answer.question.question_body
    
    class Meta:
        model = answer
        fields = ('user_answer', 'answer_body','question', 'source_url')



@admin.register(answer)
class answerAdmin(ExportActionModelAdmin, SimpleHistoryAdmin):
    resource_class = answerResource
    list_display = ['user_answer', 'question__question_title', 'answer_body', 'source_url']
    list_filter = ["user_answer", "answer_date"]
    actions = [generate_pdf]
    date_hierarchy = 'answer_date'


@admin.register(commentAnswer)
class commentAdmin(SimpleHistoryAdmin):
    list_display = ['user', 'comment_body', 'like_count']
    filter_horizontal = ('likes',)

    @admin.display(description='Количество лайков')
    def like_count(self, obj):
        return obj.likes.count()


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


# @admin.register(likesComment)
# class likesCommentAdmin(admin.ModelAdmin):
#     list_display = ['user', 'comment']