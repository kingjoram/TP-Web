from django.shortcuts import render
from .models import Questions, Answers, Tags, Users


def index(request):
    questions = Questions.objects.all()
    return render(request, 'index.html', {'questions': questions})


def question(request, question_id):
    this_question = Questions.objects.filter(id=question_id)

    question_title = this_question[0].title
    question_text = this_question[0].text
    likes_count = this_question[0].likes_count
    tags = this_question[0].tags
    answers = Answers.objects.all()

    context = \
        {'question_title': question_title,
         'question_text': question_text,
         'likes_count': likes_count,
         'answers': answers,
         'tags': tags}
    return render(request, 'question.html', context)


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')
