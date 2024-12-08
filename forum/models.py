from django.db import models


class profileAccount(models.Model):
    user_name = models.CharField(max_length= 50)
    login = models.CharField(max_length= 320)
    password = models.CharField(max_length= 256)
    email = models.EmailField(max_length= 320)
    def __str__(self):
        return self.user_name
        
    
class category(models.Model):
    category_name = models.CharField(max_length= 256)
    def __str__(self):
        return self.category_name

class question(models.Model):
    id_category = models.ForeignKey(category, on_delete=models.CASCADE)
    id_user = models.ForeignKey(profileAccount, on_delete=models.CASCADE)
    question_title = models.CharField(max_length= 100)
    question_body = models.CharField(max_length= 1000)
    question_date = models.DateField(auto_now_add=True)
    question_time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.question_title

class answer(models.Model):
    id_question = models.ForeignKey(question, on_delete=models.CASCADE)
    id_user_answer = models.ForeignKey(profileAccount, on_delete=models.CASCADE)
    answer_body = models.CharField(max_length=1000)
    answer_date = models.DateField(auto_now_add=True)
    answer_time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.answer_body

class commentAnswer(models.Model):
    id_answer = models.ForeignKey(answer, on_delete=models.CASCADE)
    id_user = models.ForeignKey(profileAccount, on_delete=models.CASCADE)
    comment_body = models.CharField(max_length=1000)
    comment_date = models.DateField(auto_now_add=True)
    comment_time = models.TimeField(auto_now_add=True)
    def __str__(self):
        return self.comment_body
    
class likesAnswer(models.Model):
    id_user = models.ForeignKey(profileAccount, on_delete=models.CASCADE)
    id_answer = models.ForeignKey(answer, on_delete=models.CASCADE)

class likesComment(models.Model):
    id_user = models.ForeignKey(profileAccount, on_delete=models.CASCADE)
    id_comment = models.ForeignKey(commentAnswer, on_delete=models.CASCADE)