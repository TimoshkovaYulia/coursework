from rest_framework import serializers
from .models import question
from .models import profileAccount
from .models import category
from .models import answer
from .models import commentAnswer



class profileSerializer(serializers.ModelSerializer):
    class Meta:
        model = profileAccount
        fields = ('user_name','email')

class categorySerializer(serializers.ModelSerializer):
    class Meta:
        model = category
        fields = ('category_name',)

class questionSerializer(serializers.ModelSerializer):
    class Meta:
        model = question
        fields = ('question_title','id_category')

class answerSerializer(serializers.ModelSerializer):
    class Meta:
        model = answer
        fields = ('answer_body','id_user_answer')

class commentSerializer(serializers.ModelSerializer):
    class Meta:
        model = commentAnswer
        fields = ('comment_body','id_user')