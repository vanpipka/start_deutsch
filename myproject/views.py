from django.http import HttpResponse, Http404, JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from services import db_backend
from django.conf import settings
from django.contrib.auth.models import User
from services.make_subscriber import make_subscriber
from django.middleware import csrf

# Опять же, спасибо django за готовую форму аутентификации.
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm

# Функция для установки сессионного ключа.
# По нему django будет определять, выполнил ли вход пользователь.
from django.contrib.auth import login as auth_login, authenticate, logout


def robots(request):

    lines = [
            "User-Agent: *",
            "Host: http://start-deutsch.ru",
            "Sitemap: http://start-deutsch.ru",
            "Disallow: /admin/",
            "User-Agent: Googlebot-Image",
            "Allow: /media/",
            "Allow: /static/img",
            "User-Agent: YandexImages",
            "Allow: /media/",
            "Allow: /static/img"
        ]

    return HttpResponse("\n".join(lines), content_type="text/plain")


def index(request):

    return render(
        request,
        'index.html',
        context={"Category": db_backend.get_all_category(),
                 "articles": db_backend.get_last_articles(5),
                 "head": "более 100+ заданий",
                 "keywords": "Задания а1"}
    )

