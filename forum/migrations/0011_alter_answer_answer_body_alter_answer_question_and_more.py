# Generated by Django 5.1.4 on 2024-12-12 14:14

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0010_historicalanswer_historicalcategory_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="answer",
            name="answer_body",
            field=models.CharField(max_length=1000, verbose_name="Содержание ответа"),
        ),
        migrations.AlterField(
            model_name="answer",
            name="question",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="answers",
                to="forum.question",
                verbose_name="Вопрос",
            ),
        ),
        migrations.AlterField(
            model_name="answer",
            name="user_answer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="forum.profile",
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="category",
            name="category_name",
            field=models.CharField(max_length=256, verbose_name="Категория"),
        ),
        migrations.AlterField(
            model_name="commentanswer",
            name="answer",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="forum.answer",
                verbose_name="Комментируемый ответ",
            ),
        ),
        migrations.AlterField(
            model_name="commentanswer",
            name="comment_body",
            field=models.CharField(
                max_length=1000, verbose_name="Содержимое комментария"
            ),
        ),
        migrations.AlterField(
            model_name="commentanswer",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="forum.profile",
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="historicalanswer",
            name="answer_body",
            field=models.CharField(max_length=1000, verbose_name="Содержание ответа"),
        ),
        migrations.AlterField(
            model_name="historicalanswer",
            name="question",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="forum.question",
                verbose_name="Вопрос",
            ),
        ),
        migrations.AlterField(
            model_name="historicalanswer",
            name="user_answer",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="forum.profile",
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcategory",
            name="category_name",
            field=models.CharField(max_length=256, verbose_name="Категория"),
        ),
        migrations.AlterField(
            model_name="historicalcommentanswer",
            name="answer",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="forum.answer",
                verbose_name="Комментируемый ответ",
            ),
        ),
        migrations.AlterField(
            model_name="historicalcommentanswer",
            name="comment_body",
            field=models.CharField(
                max_length=1000, verbose_name="Содержимое комментария"
            ),
        ),
        migrations.AlterField(
            model_name="historicalcommentanswer",
            name="user",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="forum.profile",
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="historicalprofileaccount",
            name="user_name",
            field=models.CharField(
                max_length=50,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[0-9a-zA-Zа-яА-Я ?]*$",
                        "В названии вопроса специальных символов,допустимы только буквы и цифры",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="historicalquestion",
            name="category",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="forum.category",
                verbose_name="Категория вопроса",
            ),
        ),
        migrations.AlterField(
            model_name="historicalquestion",
            name="question_body",
            field=models.CharField(max_length=1000, verbose_name="Содержание вопроса"),
        ),
        migrations.AlterField(
            model_name="historicalquestion",
            name="question_title",
            field=models.CharField(
                max_length=100,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[0-9a-zA-Zа-яА-Я ?]*$",
                        "В названии вопроса специальных символов,допустимы только буквы и цифры",
                    )
                ],
                verbose_name="Название вопроса",
            ),
        ),
        migrations.AlterField(
            model_name="historicalquestion",
            name="user",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to="forum.profile",
                verbose_name="Пользователь",
            ),
        ),
        migrations.AlterField(
            model_name="profileaccount",
            name="user_name",
            field=models.CharField(
                max_length=50,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[0-9a-zA-Zа-яА-Я ?]*$",
                        "В названии вопроса специальных символов,допустимы только буквы и цифры",
                    )
                ],
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="questions",
                to="forum.category",
                verbose_name="Категория вопроса",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="question_body",
            field=models.CharField(max_length=1000, verbose_name="Содержание вопроса"),
        ),
        migrations.AlterField(
            model_name="question",
            name="question_title",
            field=models.CharField(
                max_length=100,
                validators=[
                    django.core.validators.RegexValidator(
                        "^[0-9a-zA-Zа-яА-Я ?]*$",
                        "В названии вопроса специальных символов,допустимы только буквы и цифры",
                    )
                ],
                verbose_name="Название вопроса",
            ),
        ),
        migrations.AlterField(
            model_name="question",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="forum.profile",
                verbose_name="Пользователь",
            ),
        ),
    ]
