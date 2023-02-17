from typing import Optional, List

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
import uuid
import datetime
from django.utils import timezone


# Create your models here.
class Subscriber(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    email = models.CharField(max_length=150, default="")
    date = models.DateTimeField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.datetime.now()

        super(Subscriber, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.email)


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    name = models.CharField(max_length=150, default="")
    count = models.DecimalField(default=0, decimal_places=0, max_digits=2, blank=True)
    description = models.CharField(max_length=300, default="")
    url = models.CharField(max_length=50, default="")
    img_url = models.TextField(default="")

    def __str__(self):
        return str(self.name)

    @staticmethod
    def get_by_id(category_id: str) -> Optional["Category"]:

        category = None
        try:
            category = Category.objects.get(id=category_id)
        except ObjectDoesNotExist:
            print('cant get category with id:' + str(category_id))

        return category

    def get_as_dict(self) -> dict:
        return {"id": self.id,
                "name": self.name,
                "count": self.count,
                "description": self.description,
                "url": f"/{self.url}",
                "image": self.img_url}


class QuestionType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    name = models.CharField(max_length=150, default="")

    def __str__(self):
        return str(self.name)


class Page(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    name = models.CharField(max_length=150, default="")
    image = models.ImageField()
    position = models.DecimalField(default=0, decimal_places=0, max_digits=2, blank=True)
    right_answer = models.DecimalField(default=0, decimal_places=0, max_digits=2, blank=True)
    type = models.ForeignKey('QuestionType', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.position) + "_" + str(self.name)


class Article(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    name = models.CharField(max_length=150, default="")
    date = models.DateTimeField(auto_created=True, default=datetime.datetime.now())
    text = models.TextField(default="", blank=True)
    description = models.TextField(default="", blank=True)
    its_test = models.BooleanField(default=False, blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, blank=True,
                                 default="00000000-0000-0000-0000-000000000000")
    prev = models.ForeignKey('Article', on_delete=models.CASCADE, blank=True,
                             default="d0861558-e44f-4d78-b277-35e8098b885a")
    pages = models.ManyToManyField(Page)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return f'/article/?id={self.id}'

    def save(self, *args, **kwargs):

        self.category.count = len(Article.objects.filter(category=self.category).values('id'))
        self.category.save()

        if self.date:
            arr = Article.objects.all().filter(date__lt=self.date).order_by('-date')[:1]
        else:
            arr = Article.objects.all().order_by('-date')[:1]
        #
        for i in arr:
            self.prev = i

        super(Article, self).save(*args, **kwargs)

    def get_as_dict(self):

        min_date = timezone.now() - datetime.timedelta(days=7)

        return {"id": self.id,
                "name": self.name,
                "date": self.date,
                "text": self.text,
                "description": self.description,
                "category": Category.get_as_dict(self.category),
                "url": f"/article/?id={self.id}",
                "its_new": True if self.date > min_date else False
                }

    @staticmethod
    def get_by_id(article_id: str) -> Optional["Article"]:

        elem = None

        try:

            elem = Article.objects.get(id=article_id)

            # ==============================
            if "http://start-deutsch.ru/static/deutsch" in elem.text:
                elem.text = elem.text.replace("http://start-deutsch.ru/static/deutsch", "/static")
                elem.save()

        except ObjectDoesNotExist:
            elem = None

        return elem


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    article = models.ForeignKey(Article, on_delete=models.CASCADE, blank=True,
                                default="00000000-0000-0000-0000-000000000000")
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, default="00000000-0000-0000-0000-000000000000")
    date = models.DateTimeField()
    text = models.TextField(default="", blank=True)
    publish = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.date:
            self.date = datetime.datetime.now()

        super(Comment, self).save(*args, **kwargs)

    def get_as_dict(self) -> dict:

        return {"id": self.id,
                "date": self.date,
                "text": self.text,
                "article": self.article_id,
                "user": self.user_id,
                "accepted": self.publish,
                }


class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'article', 'publish')


class AdditionalField(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.CharField(max_length=100, default="")
    name = models.CharField(max_length=100, default="")
    phone = models.CharField(max_length=100, default="")

    def __str__(self):
        return str(self.user)

    def save(self, *args, **kwargs):
        super(AdditionalField, self).save(*args, **kwargs)

    @staticmethod
    def get_by_id(user: User) -> Optional["AdditionalField"]:

        elem = None

        try:
            elem = AdditionalField.objects.get(user=user)
        except ObjectDoesNotExist:
            elem = None

        return elem

    def save_account(self, data: dict) -> dict:

        user = data.get("user", None)

        if not user:
            return {"error": True, "error_message": "User not found"}

        self.user = user
        self.email = data.get("email", "")
        self.name = data.get("name", "")
        self.phone = data.get("phone", "")

        try:
            self.save()
            return {}
        except Exception as e:
            return {"error": True, "error_message": f"{e}"}

    def get_as_dict(self) -> dict:

        return {"id": self.id,
                "name": self.name,
                "email": self.email,
                "phone": self.phone,
                "url": f"/users/?id={self.id}"
                }


class AdditionalFieldAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'name', 'phone')
