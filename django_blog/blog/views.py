from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import auth

from .forms import LoginForm, CreateUserForm


def home(request):
    return render(request=request, template_name='blog/base.html')


def posts(request):
    pass


def login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth.login(request, user)
                return redirect('home')
    context = {'loginform': form}
    return render(request, 'blog/login.html', context=context)


def logout(request):
    auth.logout(request)
    return redirect('home')


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    context = {'registerform': form}
    return render(request, 'blog/register.html', context=context)


def profile(request):
    return HttpResponse('this is profile page')
