from django.contrib import admin

from .models import question, category, profileAccount, answer, commentAnswer

admin.site.register(question)
admin.site.register(category)
admin.site.register(profileAccount)
admin.site.register(answer)
admin.site.register(commentAnswer)