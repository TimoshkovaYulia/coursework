from rest_framework import serializers
from .models import question
from .models import profileAccount
from .models import category
from .models import answer
from .models import commentAnswer
from .models import likesComment
from .models import likesAnswer



class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profileAccount
        fields = ('user_name','email', 'login', 'password')

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('category_name',)

class questionSerializer(serializers.ModelSerializer):
    class Meta:
        model = question
        fields = ('question_title','id_category', 'id_user', 'question_body', 'question_date', 'question_time')

class answerSerializer(serializers.ModelSerializer):
    class Meta:
        model = answer
        fields = ('id', 'answer_body','id_user_answer', 'id_question', 'answer_date', 'answer_time')

class commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = commentAnswer
        fields = ('comment_body','id_user', 'id_answer', 'comment_date', 'comment_time')

class likesAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = likesAnswer
        fields = ('id_user')

class likesCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = likesComment
        fields = ('id_user','id_comment')