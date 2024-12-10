from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

alphanumeric = RegexValidator(r'^[0-9a-zA-Zа-яА-Я ]*$', 'В имени не должно содержаться специальных символов,допустимы только буквы и цифры')

class profileAccount(models.Model):
    user_name = models.CharField(max_length= 50, validators=[alphanumeric])
    login = models.CharField(max_length= 320)
    password = models.CharField(max_length= 256)
    email = models.EmailField(max_length= 320)
    def __str__(self):
        return self.user_name
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Пользователи"
        
    
class category(models.Model):
    category_name = models.CharField(max_length= 256)
    def __str__(self):
        return self.category_name
    
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

class question(models.Model):
    id_category = models.ForeignKey(category, on_delete=models.CASCADE)
    id_user = models.ForeignKey(profileAccount, on_delete=models.CASCADE)
    question_title = models.CharField(max_length= 100)
    question_body = models.CharField(max_length= 1000)
    question_date = models.DateField(auto_now_add=True)
    question_time = models.TimeField(auto_now_add=True)
    
    def __str__(self):
        return self.question_title
    
    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"
    
    def clean(self):
        if not len(self.question_body) > 15:
            raise ValidationError({'question_body': "Вопрос должен содержать не менее 15 символов"})


class answer(models.Model):
    id_question = models.ForeignKey(question, on_delete=models.CASCADE)
    id_user_answer = models.ForeignKey(profileAccount, on_delete=models.CASCADE)
    answer_body = models.CharField(max_length=1000)
    answer_date = models.DateField(auto_now_add=True)
    answer_time = models.TimeField(auto_now_add=True)
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
    id_answer = models.ForeignKey(answer, on_delete=models.CASCADE)
    id_user = models.ForeignKey(profileAccount, on_delete=models.CASCADE)
    comment_body = models.CharField(max_length=1000)
    comment_date = models.DateField(auto_now_add=True)
    comment_time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_body
    
    class Meta:
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"
    
class likesAnswer(models.Model):
    id_user = models.ForeignKey(profileAccount, on_delete=models.CASCADE)
    id_answer = models.ForeignKey(answer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Лайк на ответ"
        verbose_name_plural = "Лайки на ответ"

class likesComment(models.Model):
    id_user = models.ForeignKey(profileAccount, on_delete=models.CASCADE)
    id_comment = models.ForeignKey(commentAnswer, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Лайк на комментарий"
        verbose_name_plural = "Лайки на комментарии"