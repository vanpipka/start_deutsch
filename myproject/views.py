from django.http import HttpResponse, JsonResponse
from django.http import Http404, HttpResponseNotAllowed, HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render
from services import db_backend, make_subscriber, accounts
from django.conf import settings
from django.contrib.auth.models import User
from django.middleware import csrf
from django.contrib.auth import logout


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
        context={"category": db_backend.get_all_category(),
                 "articles": db_backend.get_last_articles(11),
                 "head": "более 100+ заданий",
                 "keywords": "Задания а1"}
    )


def article(request):

    if request.method == "POST":

        if not request.user.is_authenticated:
            raise HttpResponseNotAllowed()
        if db_backend.save_comment(request):
            return HttpResponseRedirect(request.get_full_path())
        else:
            raise HttpResponseServerError("Unknown mistake")
    else:

        article_id = request.GET.get("id", None)

        if not article_id:
            raise Http404("Article not found")

        article = db_backend.get_article(article_id)

        if not article:
            raise Http404("Article not found")

        return render(
                request,
                'blog-details.html',
                context={"categories": db_backend.get_all_category(),
                         "article": article,
                         "comments": db_backend.get_comments_by_article(request, article_id)}
            )


def subscribe(request):

    if request.method != 'POST':
        raise Http404("Page not found")

    result: bool = make_subscriber.make_subscriber(request)

    return render(
        request,
        'subscribe.html',
        context={"result": result,
                 "email": request.POST.get("email", "")}
    )


def blog(request):

    category = db_backend.get_category_by_url(request)

    if not category:
        raise Http404("Page not found")

    return render(
            request,
            "blog.html",
            context=db_backend.get_context_by_category(category)
    )


# accounts
def profile(request):

    if request.user.is_authenticated:

        return accounts.profile(request)

    else:
        return HttpResponseRedirect("/accounts/login/")


def logoff(request):

    if request.user.is_authenticated:
        logout(request)

    return HttpResponseRedirect("/")


def login(request):

    if request.user.is_authenticated:
        return HttpResponseRedirect("/accounts/profile/")

    return accounts.login(request)

