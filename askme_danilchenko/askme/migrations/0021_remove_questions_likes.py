# Generated by Django 4.2.1 on 2023-06-21 10:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0020_questions_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='likes',
        ),
    ]
