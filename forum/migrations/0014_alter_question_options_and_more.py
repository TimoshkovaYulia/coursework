# Generated by Django 5.1.4 on 2025-01-15 12:41

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0013_alter_question_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="question",
            options={
                "ordering": ["question_date"],
                "verbose_name": "Вопрос",
                "verbose_name_plural": "Вопросы",
            },
        ),
        migrations.AlterField(
            model_name="historicalquestion",
            name="category",
            field=models.ForeignKey(
                blank=True,
                choices=[
                    ("Спорт", "Спорт"),
                    ("Красота и здоровье", "Красота и здоровье"),
                    ("Образование", "Образование"),
                    ("Компьютерные игры", "Компьютерные игры"),
                    ("Семья, дом", "Семья, дом"),
                    ("Другое", "Другое"),
                ],
                db_constraint=False,
                default="Sport",
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="forum.category",
                verbose_name="Категория вопроса",
            ),
        ),
        migrations.AlterField(
            model_name="historicalquestion",
            name="question_title",
            field=models.CharField(
                max_length=100,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[0-9a-zA-Zа-яА-Я ?:]*$",
                        "В названии вопроса специальных символов,допустимы только буквы и цифры",
                    )
                ],
                verbose_name="Название вопроса",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="category",
            field=models.ForeignKey(
                choices=[
                    ("Спорт", "Спорт"),
                    ("Красота и здоровье", "Красота и здоровье"),
                    ("Образование", "Образование"),
                    ("Компьютерные игры", "Компьютерные игры"),
                    ("Семья, дом", "Семья, дом"),
                    ("Другое", "Другое"),
                ],
                default="Sport",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="forum.category",
                verbose_name="Категория вопроса",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="question_title",
            field=models.CharField(
                max_length=100,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[0-9a-zA-Zа-яА-Я ?:]*$",
                        "В названии вопроса специальных символов,допустимы только буквы и цифры",
                    )
                ],
                verbose_name="Название вопроса",
            ),
        ),
    ]
