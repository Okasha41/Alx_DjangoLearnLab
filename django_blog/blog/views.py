from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import auth

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy

from .forms import LoginForm, CreateUserForm, PostForm

from .models import Post


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


class ListView(ListView):
    model = Post
    template_name = 'blog/list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5


class DetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'


class CreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/create_form.html'
    form_class = PostForm

    def get_form_kwargs(self):
        kwargs = super().get_from_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_success_url(self):
        return reverse_lazy('detail-view', kwargs={'pk': self.object.pk})


class UpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/update.html'
    form_class = PostForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def get_success_url(self):
        return reverse_lazy('detail-view', kwargs={'pk': self.object.pk})


class DeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/delete.html'
    success_url = reverse_lazy('list-view')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
