from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomeUserModel(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(null=True)
    following = models.ManyToManyField(
        'self', symmetrical=False, related_name='followers', blank=True)

    def __str__(self):
        return self.username

    def follow(self, user):
        if user != self:
            self.following.add(user)

    def unfollow(self, user):
        if user != self:
            self.following.remove(user)

    def get_following_count(self):
        return self.following.count()

    def get_followers_count(self):
        return self.follwing.count()
