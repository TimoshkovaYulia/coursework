# Generated by Django 5.1.4 on 2024-12-11 17:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_alter_answer_question'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='questions', to='forum.category'),
        ),
    ]