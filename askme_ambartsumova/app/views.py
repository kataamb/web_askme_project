from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect
from django.core.paginator import EmptyPage, PageNotAnInteger

from django.contrib.auth.decorators import login_required

from django.contrib import auth

from app.models import*

from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import login, authenticate

from app.forms import*

from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.http import require_http_methods

from app.forms import LoginForm, RegisterForm

from django.views.decorators.csrf import csrf_protect





def paginate(objects_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)

    try:
        page_obj = paginator.page(page_num)
    except (PageNotAnInteger, EmptyPage, Exception):
        page_obj = paginator.page(1)


    return page_obj

@csrf_protect
def index(request):
    QUESTIONS = Question.objects.new_questions()

    questions = paginate(QUESTIONS, request, 2)

    #print(request.user.username)
    profile = Profile.objects.get_by_username(request.user.username)

    return render(request, template_name="index.html",
                  context={"questions": questions, "user": request.user, "profile": profile})

@csrf_protect
def hot(request):
    QUESTIONS = Question.objects.hot_questions()
    questions = paginate(QUESTIONS, request, 5)
    profile = Profile.objects.get_by_username(request.user.username)

    return render(request, template_name="hot.html",
                  context={"questions": questions, "user": request.user, "profile": profile})

@csrf_protect
@require_http_methods(['GET', 'POST'])
def log_in(request):
    if request.method == 'GET':
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():

            user = authenticate(request, **login_form.cleaned_data)

            if user:
                login(request, user)
                return redirect(reverse('index'))
        print('Failed to login')
    #return render(request, "login.html", context={"form": login_form})
    return render(request, template_name="login.html", context={"form" : login_form})

@csrf_protect
@require_http_methods(['GET', 'POST'])
def register(request):
    if request.method == 'GET':
        user_form = RegisterForm()
    if request.method == 'POST':
        user_form = RegisterForm(request.POST, request.FILES)

        if user_form.is_valid():
            user, profile = user_form.save()
            if user:
                #####create profile
                return redirect(reverse('login'))
            else:
                user_form.add_error(field=None, error="User saving error!")
    return render(request, "signup.html", {'form': user_form})


@csrf_protect
@login_required(login_url="/login/")
def logout(request):
    auth.logout(request)
    return redirect(reverse('login'))


@csrf_protect
@login_required(login_url="/login/")
def ask(request):
    profile = Profile.objects.get_by_username(request.user.username)

    if request.method == 'GET':
        question_form = QuestionForm(profile)
    if request.method == 'POST':
        question_form = QuestionForm(profile, data=request.POST)
        if question_form.is_valid():
            question = question_form.save()
            if question:
                return redirect( reverse('question', args=[question.id]) )
            else:
                question_form.add_error(field=None, error="Question saving error!")

    return render(request, template_name="ask.html",
                  context={"user": request.user, "profile": profile, 'form': question_form})

@csrf_protect
@login_required(login_url="/login/")
def settings(request):
    #print(request.user)
    #if not request.user.is_authenticated:
    #    return HttpResponseRedirect('/login/')
    profile = Profile.objects.get_by_username(request.user.username)

    return render(request, template_name="settings.html",
                  context={'user': request.user, 'profile': profile})

@csrf_protect
@login_required(login_url="/login/")
def edit_profile(request):
    profile = Profile.objects.get_by_user(request.user)
    print(profile, request.user)

    if request.method == 'GET':
        user_form = EditForm(profile)
    if request.method == 'POST':
        user_form = EditForm(profile, request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            if user:
                return redirect(reverse('index'))
            else:
                user_form.add_error(field=None, error="User saving error!")


    return render(request, template_name="edit_profile.html",
                  context={'form': user_form, 'user': request.user, "profile": profile})
    #return render(request, template_name="edit_profile.html")

@csrf_protect
@require_http_methods(['GET', 'POST'])
@login_required(login_url="/login/")
def question(request, question_id):
    profile = Profile.objects.get_by_username(request.user.username)

    question = Question.objects.get_by_pk(question_id)

    if request.method == 'GET':
        answer_form = AnswerForm(profile, question)
    if request.method == 'POST':
        answer_form = AnswerForm(profile, question, data=request.POST)
        if answer_form.is_valid():
            answer = answer_form.save()
            if answer:
                return redirect( reverse('question', args=[question.id]) )
            else:
                answer_form.add_error(field=None, error="Answer saving error!")



    ANSWERS = Answer.objects.get_by_question(question_id)
    answers = paginate(ANSWERS, request, 2)

    return render(request, template_name="question.html",
                  context={'form': answer_form, "question": question, "answers": answers,
                           'user': request.user, "profile": profile})
@csrf_protect
def tag(request, tag_slug):
    QUESTIONS = Question.objects.get_by_tag(tag_slug)
    questions = paginate(QUESTIONS, request)

    profile = Profile.objects.get_by_username(request.user.username)

    return render(request, template_name="tag.html",
                  context={"tag_name": tag_slug, "questions": questions,
                           'user': request.user, "profile": profile})

