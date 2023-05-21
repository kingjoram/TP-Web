from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import LoginForm
from .models import Questions, Answers, Tags, Users


def index(request):
    questions = Questions.objects.all()
    return render(request, 'index.html', {'questions': questions})


def question(request, question_id):
    this_question = Questions.objects.filter(id=question_id)

    question_title = this_question[0].title
    question_text = this_question[0].text
    likes_count = this_question[0].likes_count
    tags = Tags.objects.filter(questions=this_question[0])
    answers = Answers.objects.filter(question=this_question[0])

    context = \
        {'question_title': question_title,
         'question_text': question_text,
         'likes_count': likes_count,
         'answers': answers,
         'tags': tags}
    return render(request, 'question.html', context)


def ask(request):
    return render(request, 'ask.html')


def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()
    elif request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                login(request, user)
                return redirect(reverse('index'))
            login_form.add_error(None, "Invalid username or password")

    return render(request, 'login.html', context={'form': login_form})


def signup(request):
    return render(request, 'signup.html')


def tag_questions(request, tag_name):
    tag = Tags.objects.filter(name=tag_name)
    questions = Questions.objects.filter(tags=tag[0])
    context = {'tag': tag[0], 'tag_questions': questions}
    return render(request, 'tag_questions.html', context)
