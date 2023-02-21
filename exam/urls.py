
"""neva URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path
from . import views

urlpatterns = [

    path('', views.exam),

    path('result/', views.result),

    # API
    path('api/get_questions/', views.api_get_questions_by_exam),
    path('api/check_result/', views.api_get_check_result),
    path('api/make_exam/', views.api_make_exam)

    # path('api/set_words_result', views.api_set_words_result),
    # path('api/get_or_create_topic/', views.api_get_or_create_topic),

]
