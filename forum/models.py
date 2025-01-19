from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.conf import settings
from simple_history.models import HistoricalRecords 
from django.utils.text import Truncator
from django.utils import timezone
from django.urls import reverse
from django.db.models import Q
from django.forms import ModelForm

alphanumeric = RegexValidator(r'^[0-9a-zA-Zа-яА-Я ?:]*$', 'В названии вопроса специальных символов,допустимы только буквы и цифры')

# class profileAccount(models.Model):
#     user_name = models.CharField(max_length= 50, validators=[alphanumeric])
#     login = models.CharField(max_length= 320)
#     password = models.CharField(max_length= 256)
#     email = models.EmailField(max_length= 320)
#     history = HistoricalRecords()
#     def __str__(self):
#         return self.user_name
    
#     class Meta:
#         verbose_name = "Профиль"
#         verbose_name_plural = "Пользователи"

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    
    def __str__(self):
        return f'Пользователь: {self.user}'

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Пользователии"
        
    
class category(models.Model):
    category_name = models.CharField(max_length= 256, verbose_name = "Категория")
    category_image = models.ImageField(upload_to='categories/', null=True, blank=True, verbose_name="Фото категории")
    history = HistoricalRecords()

    def __str__(self):
        return self.category_name
    
    @property
    def questions_count(self):
        return self.questions.count()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

# CATEGORY_CHOICES = ( 
#     ("1", "Спорт"), 
#     ("2", "Красота и здоровье"), 
#     ("3", "Образование"), 
#     ("4", "Компьютерные игры"), 
#     ("5", "Семья, дом"), 
#     ("6", "Другое"), 
# ) choices = CATEGORY_CHOICES,default = 'Sport', 

class question(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='questions', verbose_name = "Категория вопроса")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name = "Пользователь", related_name='questions_by')
    question_title = models.CharField(max_length= 100, blank=True, default='', verbose_name = "Название вопроса", validators=[alphanumeric])
    question_body = models.CharField(max_length= 1000, verbose_name = "Содержание вопроса")
    document = models.FileField(upload_to='documents/', null=True, blank=True)
    question_date = models.DateField(auto_now_add=True)
    question_time = models.TimeField(default=timezone.now)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        if self.question_title == '':
            auto_tittle = 'без названия'
            self.question_title = auto_tittle
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.question_title
    
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ['question_date']
    
    def clean(self):
        super().clean()
        if not len(self.question_body) > 15:
            raise ValidationError({'question_body': "Вопрос должен содержать не менее 15 символов"})
        
    def get_absolute_url(self):
        return reverse('forum:question_detail',
                        args=[self.id])


class answer(models.Model):
    question = models.ForeignKey(question, on_delete=models.CASCADE, related_name='answers', verbose_name = "Вопрос")
    user_answer = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name = "Пользователь")
    answer_body = models.CharField(max_length=1000, verbose_name = "Содержание ответа")
    source_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Ссылка на источник")
    answer_date = models.DateField(auto_now_add=True)
    answer_time = models.TimeField(auto_now_add=True)
    history = HistoricalRecords()


    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
        if len(self.answer_body.split())>5:
            short_answer = Truncator(self.answer_body).words(5, truncate='...')
            print(short_answer)
            return short_answer
        else:
            return self.answer_body
    
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def clean(self):
        bad_word = 'плохое слово'
        if bad_word in self.answer_body:
            raise ValidationError({'answer_body': "Нельзя некультурно выражаться"})

class commentAnswer(models.Model):
    answer = models.ForeignKey(answer, on_delete=models.CASCADE, verbose_name = "Комментируемый ответ")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name = "Пользователь")
    comment_body = models.CharField(max_length=1000, verbose_name = "Содержимое комментария")
    comment_date = models.DateField(auto_now_add=True)
    comment_time = models.TimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile, related_name='liked_comments', blank=True)
    history = HistoricalRecords()
    def __str__(self):
        return self.comment_body
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


    
class likesAnswer(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='answer_likes')
    answer = models.ForeignKey(answer, on_delete=models.CASCADE, related_name='likes')
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Лайк на ответ"
        verbose_name_plural = "Лайки на ответ"

# class likesComment(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment_likes')
#     comment = models.ForeignKey(commentAnswer, on_delete=models.CASCADE, related_name='likes')
#     history = HistoricalRecords()

#     class Meta:
#         verbose_name = "Лайк на комментарий"
#         verbose_name_plural = "Лайки на комментарии"
