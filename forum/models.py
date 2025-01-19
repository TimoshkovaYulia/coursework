from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.conf import settings
from django.utils.text import Truncator
from django.utils import timezone
from django.urls import reverse

from simple_history.models import HistoricalRecords

alphanumeric = RegexValidator(
    r"^[0-9a-zA-Zа-яА-Я ?:]*$",
    "В названии вопроса специальных символов,допустимы только буквы и цифры",
)

class Profile(models.Model):
    ''' модель профилей '''
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        ''' перевод в текст'''
        return f"Пользователь: {self.user}"

    class Meta:
        ''' перевод'''
        verbose_name = "Профиль"
        verbose_name_plural = "Пользователии"


class category(models.Model):
    ''' модель категорий '''
    category_name = models.CharField(max_length=256, verbose_name="Категория")
    category_image = models.ImageField(
        upload_to="categories/", null=True, blank=True, verbose_name="Фото категории"
    )
    history = HistoricalRecords()

    def __str__(self):
        '''перевод в текст '''
        return self.category_name

    @property
    def questions_count(self):
        return self.questions.count()

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class question(models.Model):
    ''' модель вопросов '''
    category = models.ForeignKey(
        category,
        on_delete=models.CASCADE,
        related_name="questions",
        verbose_name="Категория вопроса",
    )
    user = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name="Пользователь",
        related_name="questions_by",
    )
    question_title = models.CharField(
        max_length=100,
        blank=True,
        default="",
        verbose_name="Название вопроса",
        validators=[alphanumeric],
    )
    question_body = models.CharField(max_length=1000, verbose_name="Содержание вопроса")
    document = models.FileField(upload_to="documents/", null=True, blank=True)
    question_date = models.DateField(auto_now_add=True)
    question_time = models.TimeField(default=timezone.now)
    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        ''' функция сохраниния автоматеически титульника вопроса '''
        if self.question_title == "":
            auto_tittle = "без названия"
            self.question_title = auto_tittle
        super().save(*args, **kwargs)

    def __str__(self):
        ''' перевод из обхекта в текст '''
        return self.question_title

    class Meta:
        '''перевод'''
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
        ordering = ["question_date"]

    def clean(self):
        ''' проверка на длину '''
        super().clean()
        if not len(self.question_body) > 15:
            raise ValidationError(
                {"question_body": "Вопрос должен содержать не менее 15 символов"}
            )

    def get_absolute_url(self):
        ''' аа '''
        return reverse("forum:question_detail", args=[self.id])


class answer(models.Model):
    ''' модель ответов '''
    question = models.ForeignKey(
        question,
        on_delete=models.CASCADE,
        related_name="answers",
        verbose_name="Вопрос",
    )
    user_answer = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    answer_body = models.CharField(max_length=1000, verbose_name="Содержание ответа")
    source_url = models.URLField(
        max_length=500, blank=True, null=True, verbose_name="Ссылка на источник"
    )
    answer_date = models.DateField(auto_now_add=True)
    answer_time = models.TimeField(auto_now_add=True)
    history = HistoricalRecords()

    @property
    def likes_count(self):
        ''' подсчет количества лайков на ответе '''
        return self.likes.count()

    def __str__(self):
        ''' сокращение представления ответа '''
        if len(self.answer_body.split()) > 5:
            short_answer = Truncator(self.answer_body).words(5, truncate="...")
            print(short_answer)
            return short_answer
        else:
            return self.answer_body

    class Meta:
        ''' перевод '''
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"

    def clean(self):
        ''' валидация цензура '''
        bad_word = "плохое слово"
        if bad_word in self.answer_body:
            raise ValidationError({"answer_body": "Нельзя некультурно выражаться"})


class commentAnswer(models.Model):
    ''' модель комментариев к ответам  '''
    answer = models.ForeignKey(
        answer, on_delete=models.CASCADE, verbose_name="Комментируемый ответ"
    )
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, verbose_name="Пользователь"
    )
    comment_body = models.CharField(
        max_length=1000, verbose_name="Содержимое комментария"
    )
    comment_date = models.DateField(auto_now_add=True)
    comment_time = models.TimeField(auto_now_add=True)
    likes = models.ManyToManyField(Profile, related_name="liked_comments", blank=True)
    history = HistoricalRecords()

    def __str__(self):
        ''' преобазование в текст '''
        return self.comment_body

    class Meta:
        ''' перевод '''
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class likesAnswer(models.Model):
    ''' модель лайки на ответы '''
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="answer_likes"
    )
    answer = models.ForeignKey(answer, on_delete=models.CASCADE, related_name="likes")
    history = HistoricalRecords()

    class Meta:
        ''' перевод  '''
        verbose_name = "Лайк на ответ"
        verbose_name_plural = "Лайки на ответ"
