from django.shortcuts import render, redirect, get_object_or_404

from django.http import HttpResponse

from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import auth

from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required

from .forms import LoginForm, CreateUserForm, PostForm, CommentForm

from .models import Post, Comment


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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_create.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        post = get_object_or_404(Post, pk=self.kwargs['pk'])
        kwargs['post'] = post
        kwargs['user'] = self.request.user
        return super().get_form_kwargs()

    def get_success_url(self):
        return reverse_lazy('comment-view', kwargs={'pk': self.object.pk})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_update.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        post = get_object_or_404(Post, pk=self.kwargs['post_pk'])
        comment = self.get_object()
        kwargs['comment'] = comment
        kwargs['post'] = post
        kwargs['user'] = self.request.user
        return super().get_form_kwargs()

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        return reverse_lazy('comment-view', kwargs={'pk': self.kwargs['post_pk']})


class ListComments(ListView):
    model = Comment
    template_name = 'blog/comment-list.html'
    ordering = ['-updated_at']
    context_object_name = 'comments'

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_id'])


class CommentDeleteView(DeleteView, LoginRequiredMixin, UserPassesTestMixin):
    model = Comment
    success_url = reverse_lazy('comments-list')

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author
