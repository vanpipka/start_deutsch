from typing import List, Optional

from myproject.models import Category, Article, Comment, AdditionalField
from myproject.forms import CommentForm

def get_last_articles(count: int) -> List:

    result = []

    for element in Article.objects.all().order_by('-date').select_related("category")[:count]:
        result.append({
            "id": element.id,
            "name": element.name,
            "date": element.date,
            "category": Category.get_as_dict(element.category),
        })

    return result


def get_all_category() -> List:
    result = []

    for element in Category.objects.all():
        if str(element.id) == '00000000-0000-0000-0000-000000000000':
            continue

        result.append(Category.get_as_dict(element))

    return result


def get_article(article_id: str) -> Optional[dict]:

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
