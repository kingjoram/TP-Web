from django.db import models
from django.contrib.auth.models import User


class QuestionManager(models.Manager):
    def get_question(self, id):
        return self.filter(id=id)


class Questions(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    likes_count = models.IntegerField(default=0)
    ask_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    object = QuestionManager
    tags = models.ManyToManyField('Tags')

class Answers(models.Model):
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey('Questions', on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    text = models.TextField(default="")


class Tags(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class Profile(models.Model):
    avatar = models.ImageField(blank=True, null=True, default='default_avatar.jpg', upload_to='avatars/%Y/%m/%d/')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
