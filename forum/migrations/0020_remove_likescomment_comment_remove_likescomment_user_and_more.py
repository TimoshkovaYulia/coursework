# Generated by Django 5.1.4 on 2025-01-17 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0019_answer_source_url_historicalanswer_source_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='likescomment',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='likescomment',
            name='user',
        ),
        migrations.AddField(
            model_name='commentanswer',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='liked_comments', to='forum.profile'),
        ),
        migrations.DeleteModel(
            name='HistoricallikesComment',
        ),
        migrations.DeleteModel(
            name='likesComment',
        ),
    ]
