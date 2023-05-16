from django.shortcuts import render
from . import models


def index(request):
    context = {'questions': models.QUESTIONS}
    return render(request, 'index.html', context)


def question(request, question_id):
    answer_context = {'answers': models.ANSWERS}
    question_context = {'question': models.QUESTIONS[question_id]}
    return render(request, 'question.html', {'question_context': question_context, 'answer_context': answer_context})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')
