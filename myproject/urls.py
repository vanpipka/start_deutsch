"""start_deutsch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import ArticleSitemap
from django.conf import settings
from django.conf.urls.static import static

sitemaps = {
    'articles': ArticleSitemap
}

urlpatterns = [

    path('admin/stats/', views.stats),
    path('api/get_stats/', views.api_get_stats),

    path('admin/', admin.site.urls),
    path('robots.txt', views.robots),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('wortschatz/', views.blog),
    path('prufungen/', views.blog),
    path('sprechen/', views.blog),
    path('horen/', views.blog),
    path('briefs/', views.blog),
    path('lesen/', views.blog),
    path('articles/', views.all_articles),

    path('article/', views.article),
    path('subscribe/', views.subscribe),

    # accounts
    path('accounts/login/', views.login),
    path('accounts/logout/', views.logoff),
    path('accounts/profile/', views.profile),

    path('quiz/', include('quiz.urls')),
    path('exam/', include('exam.urls')),

    # main
    path('', views.index),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
