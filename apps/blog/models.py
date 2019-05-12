from django.contrib.auth.models import User
from django.db import models

from apps.core.models import TimeStampObject


class Category(TimeStampObject, models.Model):
    name = models.CharField(max_length=32)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Tag(TimeStampObject, models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class Post(TimeStampObject, models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=64, unique=True)
    # symbol = models.CharField(max_length=2)
    tags = models.ManyToManyField(Tag)
    # byline = models.CharField(max_length=255)
    # background_image = models.URLField(verify_exists=True)
    slug = models.SlugField(max_length=128)
    content = models.TextField()
    publish_on = models.DateField()

    @property
    def prop_title(self):
        """
        Usage: Post.objects.get(id=1).prop_title
        :return:
        """
        title = getattr(self, "title", None)
        return title if title else None

    def __str__(self):
        return self.title
