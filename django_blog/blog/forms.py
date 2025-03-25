from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms.widgets import TextInput, PasswordInput
from .models import Post, Comment


# - Create/Register a user (Model Form)


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']


# - Authenticate a user (Model Form)

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter post title',

            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your post here',
                'rows': 5
            })
        }

    def __init__(self, *args, **kwargs):
        # Extract the user from kwargs
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        # Override save method to set the author
        instance = super().save(commit=False)
        if self.user:
            instance.author = self.user

        if commit:
            instance.save()
        return instance

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 5:
            raise forms.ValidationError(
                'Title must be at least 5 characters long')
        return title

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 10:
            raise forms.ValidationError(
                'Content must be at least 10 characters long')
        return content


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your comment here',
                'rows': 5,
            })
        }

    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post', None)
        self.user = kwargs.pop('user', None)
        self.comment = kwargs.pop('comment', None)
        return super().__init__(*args, **kwargs)

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not self.comment:
            instance.post = self.post
            instance.author = self.user
        if commit:
            instance.save()
        return instance

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) < 1:
            raise forms.ValidationError('Your comment can not be empty')
