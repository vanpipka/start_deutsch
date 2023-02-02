from typing import List

from myproject.models import Category, Article


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
