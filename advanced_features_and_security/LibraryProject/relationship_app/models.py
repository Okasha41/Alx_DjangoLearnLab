from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, AbstractBaseUser


class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title

    class Meta:
        permissions = [('can_add_book', 'Can add a new book'),
                       ('can_change_book', 'Can change edit book details'),
                       ('can_delete_book', 'Can delete a book')]


class Library(models.Model):
    name = models.CharField(max_length=255)
    books = models.ManyToManyField(Book, related_name='libraries')

    def __str__(self):
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=255)
    library = models.OneToOneField(
        Library, on_delete=models.CASCADE, related_name='librarian')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    Admin = 'Admin'
    Librarian = 'Librarian'
    Member = 'Member'
    ROLE_CHOICES = [
        (Admin, 'Admin'),
        (Librarian, 'Librarian'),
        (Member, 'Member')
    ]

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(choices=ROLE_CHOICES,
                            max_length=10, default='Member')

    def __str__(self):
        return f'{self.user.username} - {self.role}'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class CustomeUserManager(AbstractBaseUser):
    def create_user(self):
        pass

    def create_superuser(self):
        pass


class CustomeUserModel(AbstractUser):
    date_of_birth = models.DateField()
    profile_photo = models.ImageField()

    objects = CustomeUserManager()
