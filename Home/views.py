from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User as RegisterUser
from django.views.generic import View
from django import forms
from django.db.models import Q
from.forms import RegisterUserForm,SurveyPostForm,WorkshopForm,ShortCourseForm, FeedbackForm
from Home.models import RegisterUser, SurveyPost,ShortCourse ,Workshop,Feedback,News
from django.contrib import messages
from django.contrib.sessions.models import Session

def index(request):
    username = 'not logged in'
    request.session['username'] = username
    #template = loader.get_template('Home/index.html', {"username" : username})
    return render(request, 'Home/index.html', {'username': username})

def workshopDetail(request):
    username = request.session['username']
    if request.method == 'POST':
        if request.POST.get("form_type") == 'form1':
            id = request.POST.get("id")
            data = Workshop.objects.all()
            for post in data:
                post.report += 1
                post.save()
                data = Workshop.objects.filter(id=id)
                feedback = Feedback.objects.filter(eventId=id, eventType="workshop")
                return render(request, 'Home/workshopDetail.html', {'data': data, 'feedback': feedback ,'username': username})
        else:
            form = FeedbackForm(request.POST)
            feed = form.save(commit=False)
            feed.name = request.POST.get('name')
            feed.comment = request.POST.get('comment')
            feed.eventType = "workshop"
            feed.eventId = request.POST.get('eventId')
            feed.save()
            data = Workshop.objects.filter(id=(request.POST.get('eventId')))
            feedback = Feedback.objects.filter(eventId=(request.POST.get('eventId')), eventType="workshop")
            return render(request, 'Home/workshopDetail.html', {'data': data, 'feedback': feedback ,'username': username})
    else:
        id = request.GET.get("id")
        data = Workshop.objects.filter(id=id)
        feedback = Feedback.objects.filter(eventId=id, eventType="workshop")
        return render(request, 'Home/workshopDetail.html', {'data': data, 'feedback': feedback ,'username': username})

def shortcourseDetail(request):
    username = request.session['username']
    if request.method == 'POST':
        if request.POST.get("form_type") == 'form1':
            id = request.POST.get("id")
            data = ShortCourse.objects.all()
            for post in data:
                post.report += 1
                post.save()
                data = ShortCourse.objects.filter(id=id)
                feedback = Feedback.objects.filter(eventId=id, eventType="shortcourse")
                return render(request, 'Home/workshopDetail.html', {'data': data, 'feedback': feedback , 'username': username})
        else:
            form = FeedbackForm(request.POST)
            feed = form.save(commit=False)
            feed.name = request.POST.get('name')
            feed.comment = request.POST.get('comment')
            feed.eventType = "shortcourse"
            feed.eventId = request.POST.get('eventId')
            feed.save()
            data = ShortCourse.objects.filter(id=(request.POST.get('eventId')))
            feedback = Feedback.objects.filter(eventId=(request.POST.get('eventId')), eventType="shortcourse")
            return render(request, 'Home/workshopDetail.html', {'data': data, 'feedback': feedback ,'username': username})
    else:
        id = request.GET.get("id")
        data = ShortCourse.objects.filter(id=id)
        feedback = Feedback.objects.filter(eventId=id, eventType="shortcourse")
        return render(request, 'Home/workshopDetail.html', {'data': data, 'feedback': feedback ,'username': username})

def news(request):
    username = request.session['username']
    data_ordered = News.objects.all()
    data = reversed(data_ordered)
    query = request.GET.get("q")
    if query:
        data = data_ordered.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
        return render(request, 'Home/news.html', {'data': data ,'username': username})
    else:
        return render(request, 'Home/news.html', {'data': data ,'username': username})

def searchEvent(request):
    username = request.session['username']
    return render(request, 'Home/searchEvent.html', {'username': username})


def postEvent(request):
        if request.session['username'] == 'not logged in':
            username = 'not logged in'
            return render(request, 'Home/postEvent.html', {"username": username})
        else:
            username = 'logged in'
            return render(request, 'Home/postEvent.html', {"username": username})


def forgetPassword(request):
    username = request.session['username']
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if RegisterUser.objects.filter(userName = request.POST.get('userName')).exists():
            data = RegisterUser.objects.filter(userName=request.POST.get('userName'))
            for user in data:
                user.password = request.POST.get('password')
                user.save()
                return render(request, 'Home/login.html', {"username" : username})
        else:
            messages.error(request, "Incorrect Username or Password")
            return render(request, 'Home/forgetPassword.html', {"username" : username})
    else:
        form = RegisterUserForm()
        return render(request, 'Home/forgetPassword.html', {"username" : username})

def shortcourse(request):
    username = request.session['username']
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        feed = form.save(commit=False)
        feed.name = request.POST.get('name')
        feed.postTitle = request.POST.get('postTitle')
        feed.email = request.POST.get('email')
        feed.message = request.POST.get('message')
        feed.save()
        return render(request, 'Home/shortcourse.html')
    else:
        data_ordered = ShortCourse.objects.filter(status="Approved")
        data = reversed(data_ordered)
        query = request.GET.get("q")
        if query:
            data = data_ordered.filter(
                Q(title__icontains=query) |
                Q(description__icontains=query) |
                Q(SDate__icontains=query) |
                Q(venue__icontains=query)
            ).distinct()
            return render(request, 'Home/shortcourse.html', {'data': data ,'username': username})
        else:
            return render(request, 'Home/shortcourse.html', {'data': data ,'username': username})

def survey(request):
    username = request.session['username']
    data_ordered = SurveyPost.objects.filter(status = "Approved")
    data = reversed(data_ordered)
    query = request.GET.get("q")
    if query:
        data = data_ordered.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query)
        ).distinct()
        return render(request, 'Home/survey.html',{'data': data ,'username': username})
    else:
        return render(request, 'Home/survey.html', {'data': data ,'username': username})


def workshops(request):
    username = request.session['username']
    data_ordered = Workshop.objects.filter(status="Approved")
    data = reversed(data_ordered)
    query = request.GET.get("q")
    if query:
        data = data_ordered.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(SDate__icontains=query) |
            Q(venue__icontains=query)
            ).distinct()
        return render(request, 'Home/workshops.html',{'data': data ,'username': username})
    else:
        return render(request, 'Home/workshops.html', {'data': data ,'username': username})


def login(request):
    username = request.session['username']
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        if RegisterUser.objects.filter(userName=request.POST.get('userName')).exists():
            if RegisterUser.objects.filter(password=request.POST.get('password')).exists():
               request.session['username'] = username
               return render(request, 'Home/postEvent.html',{"username" : username})
        else:
            messages.error(request, "Incorrect Username or Password")
            return render(request, 'Home/login.html',{"username" : username})
    else:
            return render(request, 'Home/login.html',{"username" : username})



def registeration(request):
    username = request.session['username']
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        user = form.save(commit=False)
        user.name = request.POST.get('name')
        user.userName = request.POST.get('userName')
        user.password = request.POST.get('password')
        user.email = request.POST.get('email')
        if RegisterUser.objects.filter(userName=request.POST.get('userName')).exists():
            messages.error(request, "UserName already exists use another")
            return render(request, 'Home/registeration.html', {'form': form})
        else:
            user.save()
            return render(request, 'Home/postEvent.html', {"username" : username})
    else:
        return render(request, 'Home/registeration.html', {"username" : username})


def postsurvey(request):
    username = request.session['username']
    if request.method == 'POST':
        form = SurveyPostForm(request.POST)
        sur = form.save(commit=False)
        sur.title = request.POST.get('title')
        sur.description = request.POST.get('description')
        sur.link = request.POST.get('link')
        sur.status = "Pending"
        sur.save()
        return render(request, 'Home/index.html',{"username" : username})
    else:
        form = SurveyPostForm()
        return render(request, 'Home/postsurvey.html',{"username" : username})


def postworkshop(request):
    username = request.session['username']
    if request.method == 'GET':
        if request.session['username'] == 'not logged in':
            return render(request, 'Home/loginmsg.html',{"username" : username})
        else:
            return render(request, 'Home/postworkshop.html',{"username" : username})
    else:
        form = WorkshopForm(request.POST)
        sur = form.save(commit=False)
        sur.title = request.POST.get('title')
        sur.description = request.POST.get('description')
        sur.SDate = request.POST.get('SDate')
        sur.time = request.POST.get('time')
        sur.duration = request.POST.get('duration')
        sur.fee = request.POST.get('fee')
        sur.venue = request.POST.get('venue')
        sur.instructor = request.POST.get('instructor')
        sur.status = "Pending"
        sur.report = 0
        sur.save()
        return render(request, 'Home/searchEvent.html' ,{"username" : username})


def postshortcourse(request):
    username = request.session['username']
    if request.method == 'GET':
        if request.session['username'] == 'not logged in':
            return render(request, 'Home/loginmsg.html',{"username" : username})
        else:
            return render(request, 'Home/postshortcourse.html',{"username" : username})
    else:
        form = ShortCourseForm(request.POST)
        sur = form.save(commit=False)
        sur.title = request.POST.get('title')
        sur.description = request.POST.get('description')
        sur.SDate = request.POST.get('SDate')
        sur.time = request.POST.get('time')
        sur.duration = request.POST.get('duration')
        sur.fee = request.POST.get('fee')
        sur.venue = request.POST.get('venue')
        sur.instructor = request.POST.get('instructor')
        sur.status = "Pending"
        sur.report = 0
        sur.save()
        return render(request, 'Home/searchEvent.html',{"username" : username})



def logout(request):
    try:
        request.session['username'] = 'not logged in'
        username = request.session['username']
        return render(request, 'Home/index.html', {'username': username})
    except:
        pass
    return HttpResponse("<strong>You are logged out.</strong> go back to Home")

def loginmsg(request):
       username = request.session['username']
       return render(request, 'Home/loginmsg.html', {'username': username})