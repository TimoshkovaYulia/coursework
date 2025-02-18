# Generated by Django 5.1.4 on 2024-12-11 10:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0003_remove_answer_answer_liked_by_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="answer",
            options={"verbose_name": "Ответ", "verbose_name_plural": "Ответы"},
        ),
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name": "Категория", "verbose_name_plural": "Категории"},
        ),
        migrations.AlterModelOptions(
            name="commentanswer",
            options={
                "verbose_name": "Комментарий",
                "verbose_name_plural": "Комментарии",
            },
        ),
        migrations.AlterModelOptions(
            name="likesanswer",
            options={
                "verbose_name": "Лайк на ответ",
                "verbose_name_plural": "Лайки на ответ",
            },
        ),
        migrations.AlterModelOptions(
            name="likescomment",
            options={
                "verbose_name": "Лайк на комментарий",
                "verbose_name_plural": "Лайки на комментарии",
            },
        ),
        migrations.AlterModelOptions(
            name="profileaccount",
            options={"verbose_name": "Профиль", "verbose_name_plural": "Пользователи"},
        ),
        migrations.AlterModelOptions(
            name="question",
            options={"verbose_name": "Вопрос", "verbose_name_plural": "Вопросы"},
        ),
        migrations.AlterField(
            model_name="profileaccount",
            name="user_name",
            field=models.CharField(
                max_length=50,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[0-9a-zA-Zа-яА-Я ]*$",
                        "В имени не должно содержаться специальных символов,допустимы только буквы и цифры",
                    )
                ],
            ),
        ),
    ]
