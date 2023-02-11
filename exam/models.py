from datetime import datetime
from django.contrib import admin
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.contrib.auth.models import User
from myproject.models import Category
import uuid


# Create your models here.
class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    text = models.CharField(max_length=150, default="", blank=True)


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    text = models.CharField(max_length=150, default="", blank=True)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    text = models.CharField(max_length=150, default="", blank=True)
    image = models.ImageField(null=True, blank=True)
    itsRight = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


def encode_img(obj):
    """
    Extended encoder function that helps to serialize dates and images
    """
    if isinstance(obj, ImageFieldFile):
        try:
            return obj.url
        except ValueError as e:
            return ''

    raise TypeError(repr(obj) + " is not JSON serializable")
