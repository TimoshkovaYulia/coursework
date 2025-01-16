from rest_framework import serializers
from .models import question
from .models import Profile
from .models import category
from .models import answer
from .models import commentAnswer
from .models import likesComment
from .models import likesAnswer



class profileSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only = True, source = 'user.id')
    username = serializers.CharField(read_only = True, source = 'user.username')
    email = serializers.EmailField(read_only = True, source = 'user.email')
    first_name = serializers.CharField(read_only = True, source = 'user.first_name')
    last_name = serializers.CharField(read_only = True, source = 'user.last_name')


    class Meta:
        model = Profile
        fields = ('id','username','email', 'first_name', 'last_name')

class categorySerializer(serializers.ModelSerializer):
    questions_count = serializers.IntegerField(read_only=True,)
    class Meta:
        model = category
        fields = ('id', 'category_name','questions_count')


class answerSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True,)
    class Meta:
        model = answer
        fields = ('id', 'answer_body','user_answer', 'question', 'answer_date', 'answer_time', 'likes_count')


class questionSerializer(serializers.ModelSerializer):
    answers = answerSerializer(read_only=True, many=True)

    class Meta:
        model = question
        fields = ('id','question_title','category', 'user', 'question_body', 'question_date', 'question_time', 'answers')

class commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = commentAnswer
        fields = ('comment_body','user', 'answer', 'comment_date', 'comment_time')

class likesAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = likesAnswer
        fields = ('user','answer')

class likesCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = likesComment
        fields = ('user','comment')

