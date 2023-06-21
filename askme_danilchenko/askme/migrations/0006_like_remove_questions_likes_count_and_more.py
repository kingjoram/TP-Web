# Generated by Django 4.2.1 on 2023-06-16 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('askme', '0005_profile_avatar'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=20)),
            ],
        ),
        migrations.RemoveField(
            model_name='questions',
            name='likes_count',
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='default_avatar.jpg', null=True, upload_to='avatars/%Y/%m/%d/'),
        ),
        migrations.AddField(
            model_name='questions',
            name='likes',
            field=models.ManyToManyField(to='askme.like'),
        ),
    ]
