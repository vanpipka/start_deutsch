from typing import List, Optional
from urllib.request import Request

from myproject.models import Category, Article, Comment, AdditionalField
from django.db.models.aggregates import Max
from myproject.forms import CommentForm
from services.constants import CATEGORY_DATA
from datetime import timedelta
from django.utils import timezone


def get_last_articles(count: int) -> List:

    result = []

    for element in Article.objects.all().order_by('-date').select_related("category")[:count]:
        result.append(Article.get_as_dict(element))

    return result


def get_articles_by_category(category: Category) -> List:

    arr = []

    for e in Article.objects.all().filter(category=category).order_by('-date'):
        if str(e.id) == '00000000-0000-0000-0000-000000000000':
            continue
        arr.append(Article.get_as_dict(e))

    return arr


def get_categories_with_new_materials() -> dict:

    date = timezone.now() - timedelta(days=7)

    query = Article.objects.all().select_related("category").values('category__url').annotate(max_date=Max('date'))
    max_articles_date = {i["category__url"]: i["max_date"] for i in query if i["max_date"] > date}

    return max_articles_date


def get_all_category() -> List:
    result = []

    for element in Category.objects.all():
        if str(element.id) == '00000000-0000-0000-0000-000000000000':
            continue

        result.append(Category.get_as_dict(element))

    return result


def get_context_by_category(category: Category) -> dict:

    category_info = CATEGORY_DATA.get(category.url, {})

    return {
        "categories": get_all_category(),
        "category": category,
        "articles": get_articles_by_category(category),
        "H1": category.name,
        "description": category_info.get("description", ""),
        "head": category_info.get("head", ""),
        "keywords": category_info.get("keywords", "")}


def get_main_context(request: Request) -> dict:

    category_info = CATEGORY_DATA.get("main", {})
    page_number = request.GET.get("page", 1)

    return {
        "pagination": {"count": Article.objects.all().count(), "page_number": page_number},
        "articles": get_articles_by_page(page_number),
        "H1": "Все материалы",
        "description": category_info.get("description", ""),
        "head": category_info.get("head", ""),
        "keywords": category_info.get("keywords", "")}


def get_category_by_url(request: Request) -> Optional["Category"]:

    arr = [i for i in request.path.split("/") if i]

    if not arr:
        return None

    category = Category.objects.all().filter(url=arr[0]).first()

    return category


def get_articles_by_page(page_number: int) -> List:

    result = []
    first_order = (page_number-1)*20

    for e in Article.objects.all().order_by('-date'):  # [first_order: first_order+20]:
        if str(e.id) == '00000000-0000-0000-0000-000000000000':
            continue
        result.append(Article.get_as_dict(e))

    return result


def get_article_by_id(article_id: str) -> Optional[dict]:

    article = Article.get_by_id(article_id)

    if not article:
        return None

    return Article.get_as_dict(article)


def get_comments_by_article(request, article_id: str) -> Optional[List]:

    result = []

    users_set = set()
    comment_list = list(Comment.objects.all().filter(article=article_id).select_related("user"))

    for i in comment_list:
        users_set.add(i.user_id)

    users_info = get_users_info(list(users_set))

    for element in comment_list:

        if not element.publish and element.user != request.user:
            continue
        comment = Comment.get_as_dict(element)
        comment["user"] = users_info.get(element.user_id, {})
        result.append(comment)

    return result


def get_users_info(users: List) -> dict:

    result = {}
    for element in AdditionalField.objects.all().filter(user__in=users):
        result[element.user_id] = AdditionalField.get_as_dict(element)

    return result


def save_comment(request) -> bool:

    form = CommentForm(request.POST)
    if form.is_valid() and request.user.is_authenticated:

        article = Article.get_by_id(request.GET.get("id", ""))

        if not article:
            return False

        comment = form.save(commit=False)
        comment.user = request.user
        comment.article = article
        comment.save()
        return True

    else:
        return False


def check_object_exist(func):
    def wrapper(self, *args, **kwargs):
        if not self:
            return None
        return func(self, *args, **kwargs)
    return wrapper
