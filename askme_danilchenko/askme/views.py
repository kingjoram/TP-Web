from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import model_to_dict
from django.http import HttpResponseNotFound, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods, require_POST
from django.contrib.auth import logout

from .forms import LoginForm, SettingsForm, SignUpForm, AskForm, AnswerForm
from .models import Questions, Answers, Tags, Profile, QuestionLike, AnswerLike


def index(request):
    top_list = Answers.objects.get_top_users()

    top_users = []
    for i in range(5):
        profile_id = top_list[i].get('user')
        top_users.append(Profile.objects.get_profile_with_id(profile_id)[0])

    popular_tags = Tags.objects.get_popular_tags()
    user_avatar = '/media/default_avatar.jpg'

    if request.user.is_authenticated:
        user_profile = Profile.objects.get_profile(request.user)
        user_avatar = user_profile[0].avatar

    search_query = request.GET.get('search-text', '')

    if search_query:
        questions = Questions.objects.filter(Q(title__icontains=search_query) | Q(text__icontains=search_query)).order_by('-ask_time')
    else:
        questions = Questions.objects.all().order_by('-ask_time')

    paginator = Paginator(questions, 20)

    page_number = request.GET.get('page')

    if page_number is not None:
        if not page_number.isnumeric():
            return HttpResponseNotFound()
        if int(page_number) <= 0:
            return HttpResponseNotFound()

    page_objects = paginator.get_page(page_number)

    if Questions.objects.all().count() % 20 == 0:
        last_page = Questions.objects.all().count() / 20
    else:
        last_page = Questions.objects.all().count() / 20 + 1
    context = {
        'questions': page_objects,
        'avatar': user_avatar,
        'popular_tags': popular_tags,
        'top_users': top_users,
        'last_page': last_page.__int__()
    }
    return render(request, 'index.html', context)


def question(request, question_id):
    if request.method == 'GET':
        form = AnswerForm()
    elif request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect(reverse('login_page'))
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = Answers.objects.create(text=form.cleaned_data['text'], question=Questions.objects.get(id=question_id),
                                            user=Profile.objects.get(user_id=request.user.id))
            answer.save()
            if answer:
                return redirect(reverse("question", args=[question_id]))

    popular_tags = Tags.objects.get_popular_tags()

    this_question = Questions.objects.get_question(question_id)
    if not this_question:
        return HttpResponseNotFound()

    user_avatar = 0
    if request.user.is_authenticated:
        user_profile = Profile.objects.get_profile(request.user)
        user_avatar = user_profile[0].avatar

    tags = Tags.objects.get_question_tags(this_question[0])
    answers = Answers.objects.get_answers(this_question[0])

    paginator = Paginator(answers, 5)

    page_number = request.GET.get('page')

    if page_number is not None:
        if not page_number.isnumeric():
            return HttpResponseNotFound()
        if int(page_number) <= 0:
            return HttpResponseNotFound()

    page_objects = paginator.get_page(page_number)

    context = {
        'form': form,
        'question': this_question[0],
        'answers': page_objects,
        'tags': tags,
        'avatar': user_avatar,
        'popular_tags': popular_tags
         }
    return render(request, 'question.html', context)


@login_required(login_url="login")
@require_http_methods(['GET', 'POST'])
def ask(request):
    if request.method == 'POST':
        ask_form = AskForm(request.POST)
        if ask_form.is_valid():
            quest = Questions.objects.create(
                title=ask_form.cleaned_data['title'],
                text=ask_form.cleaned_data['text'],
                user=Profile.objects.get(user=request.user)
            )
            quest.save()
            for tag_ in ask_form.cleaned_data['tags'].split(' '):
                to_add = Tags.objects.get_or_create(name=tag_)
                quest.tags.add(to_add[0].id)
            quest.save()
            if quest:
                return redirect("question", question_id=quest.id)

    elif request.method == 'GET':
        ask_form = AskForm()

    popular_tags = Tags.objects.get_popular_tags()
    user_profile = Profile.objects.get_profile(request.user)
    user_avatar = user_profile[0].avatar
    context = {
        'form': ask_form,
        'avatar': user_avatar,
        'popular_tags': popular_tags
    }
    return render(request, 'ask.html', context)


@require_http_methods(['GET', 'POST'])
def log_in(request):
    if request.user.is_authenticated:
        return redirect('settings')

    if request.method == 'GET':
        login_form = LoginForm()
    else:
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth.authenticate(request=request, **login_form.cleaned_data)
            if user:
                login(request, user)

                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                return redirect(reverse('index'))
            login_form.add_error(None, "Invalid username or password")

    popular_tags = Tags.objects.get_popular_tags()
    context = {
        'form': login_form,
        'popular_tags': popular_tags
    }

    return render(request, 'login.html', context)


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))


@require_http_methods(['GET', 'POST'])
def signup(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'GET':
        user_form = SignUpForm()
    elif request.method == 'POST':
        user_form = SignUpForm(request.POST, files=request.FILES)
        if user_form.is_valid():
            user = User.objects.create_user(username=user_form.cleaned_data['username'],
                                            email=user_form.cleaned_data['email'],
                                            password=user_form.cleaned_data['password'],
                                            )
            user.save()
            profile = Profile.objects.create(user=user)
            profile.save()

            if user:
                login(request, user)
                return redirect(reverse('index'))
            else:
                return redirect(reverse('login'))

    popular_tags = Tags.objects.get_popular_tags()
    return render(request, 'signup.html', {"form": user_form, 'popular_tags': popular_tags})


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

    popular_tags = Tags.objects.get_popular_tags()
    context = {
        "form": form,
        'popular_tags': popular_tags
    }

    return render(request, 'settings.html', context)


def hot(request):
    govno = QuestionLike.objects.get_popular()

    questions = []
    for i in range(20):
        question_id = govno[i].get('question')
        questions.append(Questions.objects.get_question(question_id)[0])

    popular_tags = Tags.objects.get_popular_tags()

    context = {
        'questions': questions,
        'popular_tags': popular_tags
    }

    return render(request, 'hot.html', context)


def tag_questions(request, tag_name):
    popular_tags = Tags.objects.get_popular_tags()
    tag = Tags.objects.get_tag(tag_name)

    if len(tag) < 1:
        return HttpResponseNotFound()

    questions = Questions.objects.get_questions_with_tag(tag[0])

    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page')

    if page_number is not None:
        if not page_number.isnumeric():
            return HttpResponseNotFound()
        if int(page_number) <= 0:
            return HttpResponseNotFound()

    page_objects = paginator.get_page(page_number)

    context = {
        'tag': tag[0],
        'questions': page_objects,
        'popular_tags': popular_tags
    }
    return render(request, 'tag_questions.html', context)


@require_POST
@login_required(login_url='login_page', redirect_field_name="continue")
def like_question(request):
    quest_id = request.POST['question_id']
    quest = Questions.objects.get(id=quest_id)
    try:
        like = QuestionLike.objects.get(question=quest_id, user=request.user.profile.id)
    except QuestionLike.DoesNotExist:
        like = QuestionLike.objects.create(question=quest, user=request.user.profile)
        like.save()
    else:
        like.delete()

    quest.save()
    return JsonResponse(
        {'status': 'ok',
         'likes_count': quest.likes()})


@require_POST
@login_required(login_url='login_page', redirect_field_name="continue")
def like_answer(request):
    answer_id = request.POST['answer_id']
    answer = Answers.objects.get(id=answer_id)
    try:
        like = AnswerLike.objects.get(answer=answer_id, user=request.user.profile.id)
    except AnswerLike.DoesNotExist:
        like = AnswerLike.objects.create(answer=answer, user=request.user.profile)
        like.save()
    else:
        like.delete()
    answer.save()
    return JsonResponse(
        {'status': 'ok',
         'likes_count': answer.likes()})


@require_POST
@login_required()
def correct(request):
    print(1)

    answer_id = request.POST['answer_id']
    answer = Answers.objects.get(id=answer_id)

    if answer.question.get_author_id() != request.user.id:
        JsonResponse(
            {'status': 'forbidden'})
        return

    print(4)

    answer.is_correct = not answer.is_solution()
    answer.save()

    print(0)

    return JsonResponse(
            {'status': 'ok',
             'solution': f'{answer.is_solution()}'}
    )
