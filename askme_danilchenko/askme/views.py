from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.core.paginator import Paginator
from django.forms import model_to_dict
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import logout

from .forms import LoginForm, SettingsForm
from .models import Questions, Answers, Tags, Profile


def index(request):
    user_avatar = 0
    if request.user.is_authenticated:
        user_profile = Profile.objects.filter(user=request.user)
        user_avatar = user_profile[0].avatar

    questions = Questions.objects.all()
    paginator = Paginator(questions, 10)

    page_number = request.GET.get('page')

    if page_number != None:
        if not page_number.isnumeric():
            return HttpResponseNotFound()
        if int(page_number) < 0:
            return HttpResponseNotFound()

    page_objects = paginator.get_page(page_number)
    return render(request, 'index.html', {'questions': page_objects, 'avatar': user_avatar})


def question(request, question_id):
    this_question = Questions.objects.filter(id=question_id)
    if not this_question:
        return HttpResponseNotFound()

    user_avatar = 0
    if request.user.is_authenticated:
        user_profile = Profile.objects.filter(user=request.user)
        user_avatar = user_profile[0].avatar

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
         'tags': tags,
         'avatar': user_avatar}
    return render(request, 'question.html', context)


@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(['GET', 'POST'])
def ask(request):
    if not request.user.is_authenticated:
        return redirect('login')

    user_profile = Profile.objects.filter(user=request.user)
    user_avatar = user_profile[0].avatar
    context = {
        'avatar': user_avatar
    }
    return render(request, 'ask.html', context)


def log_in(request):
    if request.user.is_authenticated:
        return redirect('settings')

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

    context = {
        'form': login_form,
    }

    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

def signup(request):
    user_avatar = 0
    if request.user.is_authenticated:
        user_profile = Profile.objects.filter(user=request.user)
        user_avatar = user_profile[0].avatar
    context = {
        'avatar': user_avatar
    }
    return render(request, 'signup.html', context)


def tag_questions(request, tag_name):
    tag = Tags.objects.filter(name=tag_name)
    questions = Questions.objects.filter(tags=tag[0])
    context = {'tag': tag[0], 'tag_questions': questions}
    return render(request, 'tag_questions.html', context)


@login_required(login_url="login", redirect_field_name="continue")
@require_http_methods(['GET', 'POST'])
def settings(request):
    if request.method == 'GET':
        data = model_to_dict(request.user)
        form = SettingsForm(initial=data)
    else:
        form = SettingsForm(request.POST, files=request.FILES, instance=request.user)
        if form.is_valid():
            form.save()

    context = {
        "form": form
    }

    return render(request, 'settings.html', context)
