from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.conf import settings
from simple_history.models import HistoricalRecords 

alphanumeric = RegexValidator(r'^[0-9a-zA-Zа-яА-Я ?]*$', 'В названии вопроса специальных символов,допустимы только буквы и цифры')

class profileAccount(models.Model):
    user_name = models.CharField(max_length= 50, validators=[alphanumeric])
    login = models.CharField(max_length= 320)
    password = models.CharField(max_length= 256)
    email = models.EmailField(max_length= 320)
    history = HistoricalRecords()
    def __str__(self):
        return self.user_name
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Пользователи"

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
    history = HistoricalRecords()

    def __str__(self):
        return self.category_name
    
    @property
    def questions_count(self):
        return self.questions.count()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class question(models.Model):
    category = models.ForeignKey(category, on_delete=models.CASCADE, related_name='questions', verbose_name = "Категория вопроса")
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name = "Пользователь")
    question_title = models.CharField(max_length= 100, verbose_name = "Название вопроса", validators=[alphanumeric])
    question_body = models.CharField(max_length= 1000, verbose_name = "Содержание вопроса")
    question_date = models.DateField(auto_now_add=True)
    question_time = models.TimeField(auto_now_add=True)
    history = HistoricalRecords()
    
    def __str__(self):
        return self.question_title
    
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
    
    def clean(self):
        if not len(self.question_body) > 15:
            raise ValidationError({'question_body': "Вопрос должен содержать не менее 15 символов"})


class answer(models.Model):
    question = models.ForeignKey(question, on_delete=models.CASCADE, related_name='answers', verbose_name = "Вопрос")
    user_answer = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name = "Пользователь")
    answer_body = models.CharField(max_length=1000, verbose_name = "Содержание ответа")
    answer_date = models.DateField(auto_now_add=True)
    answer_time = models.TimeField(auto_now_add=True)
    history = HistoricalRecords()
    
    @property
    def likes_count(self):
        return self.likes.count()

    def __str__(self):
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

class likesComment(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment_likes')
    comment = models.ForeignKey(commentAnswer, on_delete=models.CASCADE, related_name='likes')
    history = HistoricalRecords()

    class Meta:
        verbose_name = "Лайк на комментарий"
        verbose_name_plural = "Лайки на комментарии"