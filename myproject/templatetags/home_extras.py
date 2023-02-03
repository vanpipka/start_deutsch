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


@register.filter(name='get_X')
def get_X(value: int) -> int:

    return 82 + ((value+1) // 2)


@register.filter(name='get_Y')
def get_Y(value: int, div: int) -> int:

    result: int = 0

    if div == 0:
        result = value*2-1
    else:
        result = value*2

    return 390+result
