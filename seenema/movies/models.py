from django.db import models
from django.conf import settings

# Create your models here.


class Movie(models.Model):
    """
    """
    name = models.CharField(max_length=100, default='N/A')
    genre = models.ForeignKey("Genre", models.PROTECT)
    release_date = models.DateTimeField(blank=True, null=True)
    upvotes = models.IntegerField(
        default=0,
        help_text="",
    )
    downvotes = models.IntegerField(
        default=0,
        help_text="",
    )
    added_on = models.DateTimeField(auto_now_add=True)
    review = models.TextField("description", blank=True)


class Genre(models.Model):
    """

    """
    name = models.CharField(max_length=50, null=True, blank=True)


class UserProfile(models.Model):
    """

    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile", verbose_name="User"
    )
    favourite_genre = models.ForeignKey("Genre", models.PROTECT, null=True, blank=True)
