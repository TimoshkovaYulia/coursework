# Generated by Django 5.1.4 on 2025-01-17 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("forum", "0018_historicalquestion_document_question_document"),
    ]

    operations = [
        migrations.AddField(
            model_name="answer",
            name="source_url",
            field=models.URLField(
                blank=True, max_length=500, null=True, verbose_name="Ссылка на источник"
            ),
        ),
        migrations.AddField(
            model_name="historicalanswer",
            name="source_url",
            field=models.URLField(
                blank=True, max_length=500, null=True, verbose_name="Ссылка на источник"
            ),
        ),
    ]
