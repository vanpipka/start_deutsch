from django import template
from django.conf import settings
from myproject.models import AdditionalField
register = template.Library()


# Регистрируем тег, с помощью которого будем получать атрибуты из файла settings
@register.simple_tag
def get_attribute(name):
    return getattr(settings, name, "")


@register.filter(name='has_group')
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter
def getname(obj):

    name = ''

    if obj.is_authenticated:

        userobject = AdditionalField.get(obj)

        if userobject != None:
            name = userobject.name

    return name


@register.filter(name='an_even_number')
def an_even_number(value: int) -> bool:

    if value % 2 == 0:
        return True

    return False


@register.filter(name='cut_text')
def cut_text(value: str) -> str:

    str_val = str(value)
    if len(str_val) >= 50:
        str_val = f"{str_val[:50]}..."

    return str_val

