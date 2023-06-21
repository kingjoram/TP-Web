from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class QuestionLikeManager(models.Manager):
    def get_popular(self):
        return self.values('question').annotate(count=Count('question')).order_by('-count')


class QuestionManager(models.Manager):
    def get_question(self, question_id):
        return self.filter(id=question_id)

    def get_questions_with_tag(self, tag):
        return self.filter(tags=tag)

    def get_hot_questions(self):
        return self.annotate(count=Count('like')).order_by('-count')


class ProfileManager(models.Manager):
    def get_profile(self, user):
        return self.filter(user=user)

    def get_profile_with_id(self, id):
        return self.filter(id=id)


class TagManager(models.Manager):
    def get_question_tags(self, question):
        return self.filter(questions=question)

    def get_tag(self, tag_name):
        return self.filter(name=tag_name)

    def get_popular_tags(self):
        return self.annotate(count=Count('questions')).order_by('-count')[:5]


class AnswerManager(models.Manager):
    def get_answers(self, question):
        return self.filter(question=question).order_by('-answer_time')

    def get_top_users(self):
        return self.values('user').annotate(count_answers=Count('id')).order_by('-count_answers')[:5]


class Profile(models.Model):
    avatar = models.ImageField(blank=True, null=True, default='default_avatar.jpg', upload_to='avatars/%Y/%m/%d/')
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=False)
    objects = ProfileManager()

    def get_name(self):
        return self.user.first_name

    def __str__(self):
        return self.user.__str__()


class QuestionLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    question = models.ForeignKey('Questions', on_delete=models.PROTECT)

    objects = QuestionLikeManager()


class AnswerLike(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    answer = models.ForeignKey('Answers', on_delete=models.PROTECT)


class Questions(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    ask_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(Profile, on_delete=models.PROTECT)
    objects = QuestionManager()
    tags = models.ManyToManyField('Tags')
    like = GenericRelation(QuestionLike)

    def likes(self):
        return QuestionLike.objects.filter(question=self.id).count()

    def get_tags(self):
        return self.tags.all()

    def get_answer_count(self):
        return Answers.objects.filter(question=self.id).count()

    def get_author(self):
        return self.user

    def get_author_id(self):
        return self.user.id


class Answers(models.Model):
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey('Questions', on_delete=models.PROTECT)
    user = models.ForeignKey(Profile, on_delete=models.PROTECT)
    text = models.TextField(default="")
    objects = AnswerManager()

    like = GenericRelation(AnswerLike)
    answer_time = models.DateTimeField(auto_now_add=True)

    def is_solution(self):
        return self.is_correct

    def get_author(self):
        return self.user

    def get_author_id(self):
        return self.user.id

    def likes(self):
        return AnswerLike.objects.filter(answer=self.id).count()


class Tags(models.Model):
    name = models.CharField(max_length=20)
    objects = TagManager()

    def __str__(self):
        return self.name
