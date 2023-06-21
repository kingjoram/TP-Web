from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from ...models import Profile, Tags, Questions, Answers, QuestionLike, AnswerLike

import random


class Command(BaseCommand):
    GENERATION_ORDER = 10

    def handle(self, *args, **options):
        self.generate_user_and_profile()
        profiles = Profile.objects.all()
        self.generate_tags()
        tags = Tags.objects.all()
        self.generate_questions(profiles)
        questions = Questions.objects.all()
        self.generate_answers(profiles, questions)
        answers = Answers.objects.all()
        self.generate_question_likes(profiles, questions)
        self.generate_answer_likes(profiles, answers)
        for question in questions:
            for i in range(3):
                question.tags.add(random.choice(tags))

    def generate_user_and_profile(self):
        def generate_user(num):
            user_dict_repr = {
                'username': f'User{num}',
                'first_name': f'Alex{num}',
                'last_name': f'Danilchenko{num}',
                'password': '1234',
                'email': f'{num}@example.com',
                'is_staff': False,
                'is_active': True,
                'is_superuser': False
            }
            return user_dict_repr
        profiles = []
        for i in range(self.GENERATION_ORDER):
            user = User.objects.create_user(**generate_user(i))
            p = Profile(user=user)
            profiles.append(p)
        Profile.objects.bulk_create(profiles)

    def generate_tags(self):
        tags = []
        for i in range(self.GENERATION_ORDER):
            t = Tags()
            t.name = f'tag{i}'
            tags.append(t)
        Tags.objects.bulk_create(tags)

    def generate_questions(self, profiles):
        questions = []
        for i in range(self.GENERATION_ORDER * 10):
            author = random.choice(profiles)
            q = Questions()
            q.title = f'Question {i}'
            q.text = f'I dont know, help me:('
            q.user = author
            questions.append(q)
        Questions.objects.bulk_create(questions)

    def generate_answers(self, profiles, questions):
        answers = []
        for i in range(self.GENERATION_ORDER * 100):
            author = random.choice(profiles)
            a = Answers()
            a.text = f'answer {i}'
            a.user = author
            a.question = random.choice(questions)
            answers.append(a)
        Answers.objects.bulk_create(answers)

    def generate_question_likes(self, profiles, questions):
        likes = []
        for i in range(self.GENERATION_ORDER * 200):
            author = random.choice(profiles)
            question = random.choice(questions)
            like = QuestionLike(user=author, question=question)
            likes.append(like)
        QuestionLike.objects.bulk_create(likes)

    def generate_answer_likes(self, profiles, answers):
        likes = []
        for i in range(self.GENERATION_ORDER * 200):
            author = random.choice(profiles)
            answer = random.choice(answers)
            like = AnswerLike(user=author, answer=answer)
            likes.append(like)
        AnswerLike.objects.bulk_create(likes)
