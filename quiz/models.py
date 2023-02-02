from datetime import datetime
from django.contrib import admin
from django.db import models
from django.db.models.fields.files import ImageFieldFile
from django.contrib.auth.models import User
from myproject.models import Category
import uuid


# Create your models here.
class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    text = models.CharField(max_length=150, default="", blank=True)
    image = models.ImageField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    part = models.IntegerField(default=0)


class Answer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    text = models.CharField(max_length=150, default="", blank=True)
    image = models.ImageField(null=True, blank=True)
    itsRight = models.BooleanField(default=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class Topic(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    text = models.CharField(max_length=150, default="", blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return str(self.text)

    def to_dict(self):

        return {
            "text": self.text,
            "id": self.id,
            "image": encode_img(self.image)
        }

    @staticmethod
    def get_by_id(item_id):

        try:
            topic = Topic.objects.get(id=item_id)
            return topic.to_dict()
        except:
            print('cant get topic with id:' + str(item_id))

        return None


    @staticmethod
    def get_or_create_by_name(item_name):

        q = Topic.objects.all().filter(text=item_name)

        if len(q) == 0:
            # create new
            topic = Topic()
            topic.text = item_name
            topic.save()
            return topic.to_dict()
        else:
            return q[0].to_dict()

        return None


class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    quiz_type = models.CharField(max_length=150, default="", blank=True)
    right_answers = models.IntegerField(default=0, blank=True)
    question_count = models.IntegerField(default=0, blank=True)
    additional = models.TextField(default="", null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()

    def save(self, *args, **kwargs):

        if not self.date:
            self.date = datetime.now()

        super(Result, self).save(*args, **kwargs)


class ResultAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'right_answers', 'question_count')


class Word(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    text = models.CharField(max_length=150, default="", blank=True)
    translation = models.CharField(max_length=150, default="", blank=True)
    image = models.ImageField(null=True, blank=True)
    subject = models.ForeignKey(Topic, on_delete=models.CASCADE)


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