# Generated by Django 4.2.1 on 2023-06-16 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0007_delete_like_alter_questions_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='questions',
            name='likes',
        ),
        migrations.AddField(
            model_name='profile',
            name='likes',
            field=models.ManyToManyField(to='askme.questions'),
        ),
    ]