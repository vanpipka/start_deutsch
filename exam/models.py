from datetime import datetime
from typing import Optional

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.fields.files import ImageFieldFile, FieldFile
from services.db_backend import check_object_exist
from myproject.models import Category
import uuid


class Exam(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    name = models.CharField(max_length=150, default="", blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_created=True, default=datetime.now())
    audio = models.FileField(null=True, blank=True)

    def __str__(self):
        return f"{self.name} / {self.category}"

    @check_object_exist
    def get_as_dict(self):

        return {"id": self.id,
                "name": self.name,
                "category": Category.get_as_dict(self.category),
                "date": self.date,
                "audio": encode_audio(self.audio),
                "url": f"/exam/?id={self.id}",
                }

    @staticmethod
    def get_by_id(exam_id: str) -> Optional["Exam"]:

        try:
            elem = Exam.objects.get(id=exam_id)
        except ObjectDoesNotExist:
            elem = None
        return elem


class ExamFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'id', 'date')


class Section(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    text = models.CharField(max_length=150, default="", blank=True)
    description = models.TextField(default="", blank=True)
    order = models.IntegerField(default=0)
    type = models.CharField(max_length=15, default="A B C", blank=True)

    def __str__(self):
        return f"{self.order}. {self.text} / {self.description[:20]}..."

    @check_object_exist
    def get_as_dict(self):
        return {"id": self.id,
                "text": self.text,
                "description": self.description,
                "order": self.order,
                }


class SectionFieldAdmin(admin.ModelAdmin):
    list_display = ('order', 'text', 'description')


class Question(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    text = models.CharField(max_length=150, default="", blank=True)
    order = models.IntegerField(default=0)
    image = models.ImageField(null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, null=True)
    right_answer = models.IntegerField(default=0)

    @check_object_exist
    def get_as_dict(self):

        return {"id": self.id,
                "text": self.text,
                "order": self.order,
                "image": encode_img(self.image),
                "section": Section.get_as_dict(self.section),
                "answers": [i for i in self.section.type.split(" ")],
                "right": self.right_answer,
                }

    def __str__(self):
        return f"{self.order}. {self.section}/{self.exam}/{self.id}"


class QuestionFieldAdmin(admin.ModelAdmin):
    list_display = ('order', 'id', 'section', 'exam')


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


def encode_audio(obj):

    print(type(obj))
    """
    Extended encoder function that helps to serialize dates and images
    """
    if isinstance(obj, FieldFile):
        try:
            return obj.url
        except ValueError as e:
            return ''

    raise TypeError(repr(obj) + " is not JSON serializable")