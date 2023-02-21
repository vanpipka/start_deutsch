from datetime import datetime
from typing import Optional

from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models.fields.files import ImageFieldFile, FieldFile
from django.contrib.auth.models import User
from myproject.models import Category, Record
from services.common_services import check_if_new, check_object_exist
import uuid


class Exam(Record):

    audio = models.FileField(null=True, blank=True)

    @check_object_exist
    def get_as_dict(self):

        return {"id": self.id,
                "name": self.name,
                "category": Category.get_as_dict(self.category),
                "date": self.date,
                "audio": encode_audio(self.audio),
                "url": f"/exam/?id={self.id}",
                "its_new": check_if_new(self.date)
                }

    @staticmethod
    def get_by_id(exam_id: str) -> Optional["Exam"]:

        try:
            elem = Exam.objects.get(id=exam_id)
        except ObjectDoesNotExist:
            elem = None
        return elem


class ExamFieldAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'date')


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

    @staticmethod
    def get_by_id(exam_id: str) -> Optional["Question"]:

        try:
            elem = Question.objects.get(id=exam_id)
        except ObjectDoesNotExist:
            elem = None
        return elem

    @check_object_exist
    def get_as_dict(self):

        return {"id": self.id,
                "text": self.text,
                "order": self.order,
                "image": encode_img(self.image),
                "section": Section.get_as_dict(self.section),
                "answers": [i for i in self.section.type.split(" ")],
                }

    def __str__(self):
        return f"{self.order}. {self.section}/{self.exam}/{self.id}"


class QuestionFieldAdmin(admin.ModelAdmin):
    list_display = ('order', 'id', 'section', 'exam')


class Result(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    try_id = models.UUIDField(default=uuid.uuid4, help_text="Unique ID")
    date = models.DateTimeField(auto_created=True, default=datetime.now())
    user = models.ForeignKey(User, related_name="user", on_delete=models.CASCADE, null=True, blank=True)
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.IntegerField(default=0)

    @staticmethod
    @check_object_exist
    def get_by_try(try_id: str) -> []:

        q = Result.objects.all().filter(try_id=try_id).select_related("question").select_related("exam")\
            .order_by("question__order")
        exam_data = None
        questions = []

        for i in q:
            if not exam_data:
                exam_data = Exam.get_as_dict(Exam.get_by_id(i.exam_id))

            question = Question.get_as_dict(Question.get_by_id(i.question_id))
            if not question:
                continue
            question["its_right"] = i.question.right_answer == i.answer
            question["answer"] = question["answers"][i.answer]
            question["right_answer"] = question["answers"][i.question.right_answer]
            questions.append(question)

        return {"exam": exam_data, "questions": questions}


class ResultFieldAdmin(admin.ModelAdmin):
    list_display = ('try_id', 'date' , 'user', 'exam', 'question', 'answer')


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