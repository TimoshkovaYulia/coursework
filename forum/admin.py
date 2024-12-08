from django.contrib import admin

from .models import question, category, profileAccount, answer, commentAnswer, likesAnswer, likesComment


admin.site.register(profileAccount)
admin.site.register(category)
admin.site.register(question)
admin.site.register(answer)
admin.site.register(commentAnswer)
admin.site.register(likesAnswer)
admin.site.register(likesComment)